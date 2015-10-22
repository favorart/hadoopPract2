package org.myorg;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;


public class PageRankPrepare
{
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, IntWritable, Text>
    {   
        public void map(LongWritable key,
        				Text value,
        				OutputCollector<IntWritable, Text> output,
        				Reporter reporter
        			   ) throws IOException
        {
            String[] data = value.toString().split(",");
            if (data.length == 2 && data[0].charAt(0) != '"')
            { output.collect(new IntWritable(Integer.parseInt(data[0])), new Text(data[1])); }
        }
    }
    
    public static class Reduce extends MapReduceBase implements Reducer<IntWritable, Text, IntWritable, Text>
    {    
    	private static final double alpha = 0.15;
        public void reduce(IntWritable key, // doc_id
        				   Iterator<Text> values,
        				   OutputCollector<IntWritable, Text> output,
        				   Reporter reporter
        				  ) throws IOException
        {
            String docs = values.next().toString();            
            while(values.hasNext())
            { docs = docs.concat(String.format( ",%s", values.next().toString() )); }
            output.collect(key, new Text(String.format("%f\t%s", alpha, docs)));
        }
    }
}
