import org.apache.flink.streaming.api.functions.sink.filesystem.StreamingFileSink
import org.apache.flink.core.fs.Path
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.watermark.Watermark
import org.apache.flink.streaming.connectors.file.FileSink
import org.apache.flink.streaming.connectors.file.FileSink.RowFormatBuilder
import org.apache.flink.streaming.api.functions.sink.filesystem.OutputFileConfig
import org.apache.flink.streaming.api.functions.sink.filesystem.bucketassigners.SimpleVersionedStringSerializer
import org.apache.flink.streaming.api.functions.sink.filesystem.rollingpolicies.DefaultRollingPolicy
import org.apache.flink.streaming.api.functions.sink.filesystem.bucketassigners.DateTimeBucketAssigner

object WordCount {

  val wordCountData: List[String] = List(
    "To be, or not to be,--that is the question:--",
    "Whether 'tis nobler in the mind to suffer",
    "The slings and arrows of outrageous fortune",
    "Or to take arms against a sea of troubles,",
    "And by opposing end them?--To die,--to sleep,--",
    "No more; and by a sleep to say we end",
    "The heartache, and the thousand natural shocks",
    "That flesh is heir to,--'tis a consummation",
    "Devoutly to be wish'd. To die,--to sleep;--",
    "To sleep! perchance to dream:--ay, there's the rub;",
    "For in that sleep of death what dreams may come,",
    "When we have shuffled off this mortal coil,",
    "Must give us pause: there's the respect",
    "That makes calamity of so long life;",
    "For who would bear the whips and scorns of time,",
    "The oppressor's wrong, the proud man's contumely,",
    "The pangs of despis'd love, the law's delay,",
    "The insolence of office, and the spurns",
    "That patient merit of the unworthy takes,",
    "When he himself might his quietus make",
    "With a bare bodkin? who would these fardels bear,",
    "To grunt and sweat under a weary life,",
    "But that the dread of something after death,--",
    "The undiscover'd country, from whose bourn",
    "No traveller returns,--puzzles the will,",
    "And makes us rather bear those ills we have",
    "Than fly to others that we know not of?",
    "Thus conscience does make cowards of us all;",
    "And thus the native hue of resolution",
    "Is sicklied o'er with the pale cast of thought;",
    "And enterprises of great pith and moment,",
    "With this regard, their currents turn awry,",
    "And lose the name of action.--Soft you now!",
    "The fair Ophelia!--Nymph, in thy orisons",
    "Be all my sins remember'd."
  )

  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment
    env.setRuntimeMode(RuntimeExecutionMode.BATCH)
    env.setParallelism(1)

    val inputPath: Option[String] = Option(args.lift(0).getOrElse(null))
    val outputPath: Option[String] = Option(args.lift(1).getOrElse(null))

    val ds = if (inputPath.isDefined) {
      env.readTextFile(inputPath.get)
        .assignTimestampsAndWatermarks(new WatermarkStrategy[String] {
          override def createWatermarkGenerator(context: WatermarkGeneratorSupplier.Context): WatermarkGenerator[String] = {
            new WatermarkGenerator[String] {
              override def onEvent(event: String, eventTimestamp: Long, output: WatermarkOutput): Unit = {}

              override def onPeriodicEmit(output: WatermarkOutput): Unit = {
                output.emitWatermark(new Watermark(Long.MaxValue))
              }
            }
          }
        })
    } else {
      println("Executing word_count example with default input data set.")
      println("Use --input to specify file input.")
      env.fromCollection(wordCountData)
    }

    val wordCountResult = ds.flatMap(_.split("\\s+"))
      .map((_, 1))
      .keyBy(0)
      .reduce((a, b) => (a._1, a._2 + b._2))

    if (outputPath.isDefined) {
      val outputFileConfig = OutputFileConfig.builder()
        .withPartPrefix("prefix")
        .withPartSuffix(".ext")
        .build()

      val fileSink: StreamingFileSink[(String, Int)] = StreamingFileSink
        .forRowFormat(new Path(outputPath.get), new SimpleStringEncoder[(String, Int)]("UTF-8"))
        .withOutputFileConfig(outputFileConfig)
        .build()

      wordCountResult.addSink(fileSink)
    } else {
      println("Printing result to stdout. Use --output to specify output path.")
      wordCountResult.print()
    }

    env.execute("WordCount")
  }
}
