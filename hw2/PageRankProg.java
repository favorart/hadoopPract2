package org.myorg;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;

import org.myorg.PageRank;
import org.myorg.PageRankPrepare;


public class PageRankProg
{
    public static void  main(String[] args) throws Exception
	{
		// Settings
        JobConf conf = new JobConf(PageRankPrepare.class);
        conf.setJobName("PageRankPrepare_java");

        // Out format for map
        conf.setMapOutputKeyClass(IntWritable.class);
        conf.setMapOutputValueClass(Text.class);
        // Out format for reduce
        conf.setOutputKeyClass(IntWritable.class);
        conf.setOutputValueClass(Text.class);

        // MapRed
        conf.setMapperClass(PageRankPrepare.Map.class);
        conf.setReducerClass(PageRankPrepare.Reduce.class);

        // External formats
        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);

        //  Preparations
        Path  inputPath = null;
        Path outputPath = new Path("PageRankStep_0_java");
        
        if (args.length > 0)
        { inputPath = new Path(args[0]); }
        else
        { inputPath = new Path("/data/patents/cite75_99.txt"); }
        
        FileInputFormat.setInputPaths(conf, inputPath);
        FileOutputFormat.setOutputPath(conf, outputPath);

        FileSystem fs = FileSystem.get(conf);
        if ( fs.exists(outputPath) )
        {
        	// recursive file delete
        	fs.delete(outputPath, true);
        }
        
        JobClient.runJob(conf);

        // PageRank algorithm itself
        conf = new JobConf(PageRank.class);
        
        conf.setMapOutputKeyClass(IntWritable.class);
        conf.setMapOutputValueClass(Text.class);
        conf.setOutputKeyClass(IntWritable.class);
        conf.setOutputValueClass(Text.class);
        
        conf.setMapperClass(PageRank.Map.class);
        conf.setReducerClass(PageRank.Reduce.class);
        
        conf.setInputFormat(TextInputFormat.class);
        conf.setOutputFormat(TextOutputFormat.class);
        
        int loop = 30;
        if ( args.length > 1 )
        { loop = Integer.parseInt(args[1]); }
        
        fs = FileSystem.get(conf);
        for (int i = 1; i <= loop; ++i)
        {
            conf.setJobName(String.format("PageRankStep_%1$d_java", i));
            
            inputPath = outputPath;
            outputPath = new Path(String.format("PageRank_Step_%1$d_java", i));
            if ( fs.exists(outputPath) )
            {
            	// recursive file delete
                fs.delete(outputPath, true);
            }
            
            FileInputFormat.setInputPaths(conf, inputPath);
            FileOutputFormat.setOutputPath(conf, outputPath);

            JobClient.runJob(conf);
            
            // recursive file delete
            fs.delete(inputPath, true);
        }
    }
}
