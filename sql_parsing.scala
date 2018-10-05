// This program will process a SQL and print out the Select and group by with possible table source from the SQL.
// It will help in identifying the most commonly used attribute  and group by for creating aggregates.
// List the tables in the SQL as some are only used for joining and no attributes are selected.

//import java.io.File
import java.io._
import java.nio.file.{Paths, Files}

import scala.io.Source

object sqlformat extends App{

   case class SqlDetails(sqlName: String, attribute: Option[String] = None,alias:Option[String] = None, recordType:String, tableName :String)

    var tableMap = scala.collection.mutable.HashMap.empty[String,String]

    val selectpat = "select.*".r;   var selectStr = ""; var processAttribute:String = ""

    val frompat = ".*from.*".r;  var fromStr = ""

    val wherepat = ".*where.*".r; var whereStr = ""

    val groupbypat = ".*group by.*".r; var groupbyStr = ""

    val orderbypat = ".*order by.*".r; var orderbyStr = ""

    var attributes: String = "";  var filename = "mysql3.sql"
//    var filelist = List.empty[File]

//    getSelectCount if Select count is > 1 then there is a sub query involved
//    getWithCount if With involved then also it has a sub query , it could be on one table.
//    getInsertCount
//    getUpdateCount
//    getDeleteCount

    var outData = List.empty[SqlDetails]

  val folder = "C:\\myScalaA\\sql"
//  val folder = "C:\\Mywork\\Compare\\AA-Work\\sqlsx"

   Files.exists(Paths.get(folder)) match {
     case false => println("Folder does not exist")
     case _ => ""
   }

  val d = new File(folder)

  val filelist: List[File] = if (d.exists && d.isDirectory) d.listFiles.filter(_.isFile).toList.filter{file => file.toString.endsWith(".sql")} else List.empty[File]

  for (filenamelist <- filelist) {

    processAttribute = "";selectStr = ""; fromStr = "";whereStr="";groupbyStr = "";orderbyStr = ""; tableMap = tableMap.empty

    filename = filenamelist.toString
    val bufferedSource = Source.fromFile(filename)

    filename = filename.replace(folder+"\\","")

    var outbuffer = ""
    for (line <- bufferedSource.getLines) {
      outbuffer += line.trim.toLowerCase.replaceAll(" +", " ").replace("select", "select\n")
        .replace("from", "\nfrom\n")
        .replace("where", "\nwhere\n")
        .replace("group by", "\ngroup by\n")
        .replace("order by", "\norder by\n")

    }

    bufferedSource.close

    for (lowercaseLine <- outbuffer.split("\n")) {

      lowercaseLine match {
        case selectpat(_*) => processAttribute = "select"
        case frompat(_*) => processAttribute = "from"
        case wherepat(_*) => processAttribute = "where"
        case groupbypat(_*) => processAttribute = "group by"
        case orderbypat(_*) => processAttribute = "order by"
        case _ => ""
      }

      processAttribute match {
        case "select" => if (lowercaseLine != "select") {
          selectStr += " " + lowercaseLine
        }
        case "from" => if (lowercaseLine != "from") {
          fromStr += " " + lowercaseLine
        }
        case "where" => if (lowercaseLine != "where") {
          whereStr += " " + lowercaseLine
        }
        case "group by" => if (lowercaseLine != "group by") {
          groupbyStr += " " + lowercaseLine
        }
        case "order by" => if (lowercaseLine != "order by") {
          orderbyStr += " " + lowercaseLine
        }
        case _ => ""
      }

    }

    val inStr = fromStr.replace("inner join", ",")
      .replace("left outer join", ",")
      .replace("right outer join", ",")
      .replace("left join", ",")
      .replace("right join", ",")
      .replace("full outer join", ",")
      .split(",")

    //creating a mutable hash map of alias and table name from the FROM clause of the SQL
    for (rawtab <- inStr) {
      val tab = if (rawtab.contains(" on ")) rawtab.split(" on ")(0) else rawtab
      tab.trim match {
        case x if x.contains(" as ") => val splited = x.split(" as ")
          tableMap += (splited(1).trim -> splited(0))
        case x if x.contains(" ") => val splited = x.split(" ")
          tableMap += (splited(1).trim -> splited(0))
        case x => tableMap += (x.trim -> x)
      }
    }


//adding as to the alias name if not present to be consistent
val addas = (inStringval :String)  => {
  val inString = inStringval.replace (" +", " ").trim
  inString match {
    case x if x.split(" ").length > 1 &&  ! x.contains(" as ") =>
      val myLast = x.split(" ").last
      val outString = if ((Array("end", ")") contains myLast)
        || (Array(')', ']') contains myLast.last.toChar)) x + " as AliasNotDefined" else x.replace(" " + myLast, " as " + myLast)
      outString
    case x => x
  }
}


// takeing care of computed metrics in the Select and group by
val processSelect = (inStr: String, intype: String) => {
                var currentAttribute = ""
                var attributeArray = Array.empty[String]
                var noBrackets = 0

                for (char <- inStr) {
                //      println(char)
                if (char == '(') {
                noBrackets += 1
                currentAttribute += char
              }
                else if (char == ')') {
                noBrackets -= 1
                currentAttribute += char
              }
                else if (char == ',' && noBrackets == 0) {
                //attributeList = attributeList ::: List(currentAttribute)
                  attributeArray = attributeArray :+ (if (intype == "select" ) {addas(currentAttribute) } else currentAttribute)
                  currentAttribute = ""
              } else {
                currentAttribute += char
              }
              }
                attributeArray = attributeArray :+ (if (intype == "select" ) {addas(currentAttribute) } else currentAttribute)

              attributeArray
    }

    var tableName = ""

    val attributeArray = processSelect(selectStr, "select")
    for (att <- attributeArray) {

      tableName = tableMap.values.toList.mkString(",")
      att.trim match {
        case x if x.contains(" as ") => val splitValue = x.split(" as ")
          if (splitValue(0).contains(".")) {
            tableName = tableMap.getOrElse(splitValue(0).split("\\.")(0), tableName)
          }
          outData = outData ::: List(SqlDetails(sqlName = filename, attribute = Some(splitValue(0)), alias = Some(splitValue(1)), recordType = "select", tableName = tableName))

        case x if x.contains(" ") => val splitValue = x.split(" ")

          if (splitValue.length == 2) {

            if (splitValue(0).contains(".")) {
              tableName = tableMap.getOrElse(splitValue(0).split("\\.")(0), tableName)
            }
            outData = outData ::: List(SqlDetails(sqlName = filename, attribute = Some(splitValue(0)), alias = Some(splitValue(1)), recordType = "select", tableName = tableName))
          } else {println(x)}
        case x =>
          if (x.contains(".")) {
            tableName = tableMap.getOrElse(x.split("\\.")(0), tableName)
          }
          outData = outData ::: List( SqlDetails(sqlName = filename, attribute = Some(x), alias = Some(x), recordType = "select", tableName = tableName))
      }

    }

    val groupbyattributeArray = processSelect(groupbyStr,"groupby")
    for (att <- groupbyattributeArray) {
      tableName = tableMap.values.toList.mkString(",")
      val atttrim = att.trim
      if (atttrim.contains(".")) {
        tableName = tableMap.getOrElse(atttrim.split("\\.")(0),tableName)
      }
      outData = outData ::: List( SqlDetails(sqlName = filename, attribute = Some(atttrim), alias = Some(atttrim), recordType = "group by", tableName = tableName))
    }


    for ((key,value) <- tableMap) {
      outData = outData ::: List( SqlDetails(sqlName = filename, attribute = None, alias = None, recordType = "tables", tableName = value))
    }

    //    println(selectStr)
    //    println(fromStr)
    //    println(whereStr)
    //    println(groupbyStr)
    //    println(orderbyStr)
  }

  val  fw =new FileWriter("C:\\Mywork\\Compare\\AA-Work\\sqls\\mydata2.out",true)
  for (list1 <- outData){
//    println(list1.sqlName +"\t"+ list1.attribute.getOrElse(None)+"\t"+ list1.alias.getOrElse(None) +"\t"+ list1.recordType +"\t"+ list1.tableName)
    fw.write(list1.sqlName +"\t"+ list1.attribute.getOrElse(None)+"\t"+ list1.alias.getOrElse(None) +"\t"+ list1.recordType +"\t"+ list1.tableName +"\n")
  }
  fw.close()

  }
