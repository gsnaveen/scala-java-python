// This program will process a SQL and print out the Select and group by with possible table source from the SQL.
// It will help in identifying the most commonly used attribute  and group by for creating aggregates.
// List the tables in the SQL as some are only used for joining and no attributes are selected.

import java.io.File

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
    var filelist = List.empty[File]

//    getSelectCount if Select count is > 1 then there is a sub query involved
//    getWithCount if With involved then also it has a sub query , it could be on one table.
//    getInsertCount
//    getUpdateCount
//    getDeleteCount

//    var outData: List[Product with Serializable]

    var outData = List.empty[SqlDetails]

  val folder = "C:\\myScalaA\\sql"
  val d = new File(folder)
  if (d.exists && d.isDirectory) {
    filelist = d.listFiles.filter(_.isFile).toList.filter{file => file.toString.endsWith(".sql")}
  }

  for (filenamelist <- filelist) {

    processAttribute = "";selectStr = ""; fromStr = "";whereStr="";groupbyStr = "";orderbyStr = ""; tableMap = tableMap.empty

    filename = filenamelist.toString
    val bufferedSource = Source.fromFile(filename)

    filename = filename.replace(folder+"\\","")

    var outbuffer = ""
    for (line <- bufferedSource.getLines) {
      outbuffer += line.trim.replaceAll(" +", " ").toLowerCase.replace("select", "select\n")
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
      }

    }

    val inStr = fromStr.replace("inner join", ",")
      .replace("left outer join", ",")
      .replace("right outer join", ",")
      .replace("full outer join", ",")
      .split(",")

    for (rawtab <- inStr) {
      var tab = rawtab
      if (rawtab.contains(" on ")) {
        tab = rawtab.split(" on ")(0)
      }

      tab.trim match {
        case x if x.contains(" as ") => val splited = x.split(" as ")
          tableMap += (splited(1).trim -> splited(0))
        case x if x.contains(" ") => val splited = x.split(" ")
          tableMap += (splited(1).trim -> splited(0))
        case x => tableMap += (x.trim -> x)
      }
    }

//    print(tableMap)

    //selectStr.split(",").foreach(println)
    var tableName = ""

    for (att <- selectStr.split(",")) {
      tableName = tableMap.values.toList.mkString(",")
//      println(att)
      att.trim match {
        case x if x.contains(" as ") => val splitValue = x.split(" as ")
          if (splitValue(0).contains(".")) {
            tableName = tableMap.getOrElse(splitValue(0).split("\\.")(0), tableName)
          }
          outData = outData ::: List(SqlDetails(sqlName = filename, attribute = Some(splitValue(0)), alias = Some(splitValue(1)), recordType = "select", tableName = tableName))

        case x if x.contains(" ") => val splitValue = x.split(" ")
          if (splitValue(0).contains(".")) {
            tableName = tableMap.getOrElse(splitValue(0).split("\\.")(0), tableName)
          }
          outData = outData ::: List(new SqlDetails(sqlName = filename, attribute = Some(splitValue(0)), alias = Some(splitValue(1)), recordType = "select", tableName = tableName))
        case x =>
          if (x.contains(".")) {
            tableName = tableMap.getOrElse(x.split("\\.")(0), tableName)
          }
          outData = outData ::: List(new SqlDetails(sqlName = filename, attribute = Some(x), alias = Some(x), recordType = "select", tableName = tableName))
      }

    }

    for (att <- groupbyStr.split(",")) {
      val atttrim = att.trim
      if (atttrim.contains(".")) {
        tableName = tableMap(atttrim.split("\\.")(0))
      }
      outData = outData ::: List(new SqlDetails(sqlName = filename, attribute = Some(atttrim), alias = Some(atttrim), recordType = "group by", tableName = tableName))
    }


    for ((key,value) <- tableMap) {
      outData = outData ::: List(new SqlDetails(sqlName = filename, attribute = None, alias = None, recordType = "tables", tableName = value))
    }

       for (list1 <- outData){
        println(list1.sqlName +"\t"+ list1.attribute.getOrElse(None)+"\t"+ list1.alias.getOrElse(None) +"\t"+ list1.recordType +"\t"+ list1.tableName.replace("List(","").replace(")",""))
      }

//    outData.foreach(println)
    //  groupbyStr.split(",").foreach(println)
    //
    //    println(selectStr)
    //    println(fromStr)
    //    println(whereStr)
    //    println(groupbyStr)
    //    println(orderbyStr)
  }
  }
