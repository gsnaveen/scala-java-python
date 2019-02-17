import collection.breakOut
import scala.util.parsing.json._

object listTest extends App{

  val mystr = "1,2,3,4,5,6,7"
  val trimmedList: List[String]  = mystr.split(",").map(_.trim)(breakOut)
  println(trimmedList)

  val result = trimmedList.slice(0, trimmedList.size - 1)
  
  println(result)
  val y = 10
  var pushnum =0
  if (y == 10) {
    pushnum = 1
  }
  
  val return_Result = pushnum::result
  println(return_Result)
  println(return_Result.lift(2))

  println(return_Result.lift(2)_)

  if (return_Result.lift(2).getOrElse(-1) == 2){
    println("it is 2")
  }

  val dt = 1549152000
//  println(dt.toDateTime)
  val parsed = JSON.parseFull("""{"Name":"abc", "age":10}""")
  val parsedlist = JSON.parseFull("""[1,2,3,4,5,6,7]""")

  println(parsed)
  println(parsedlist)

  for (i <- parsedlist) {
    println(i)
  }

  parsedlist.foreach{println}
