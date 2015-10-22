package org.myorg;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.conf.*;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapred.*;
import org.apache.hadoop.util.*;


public class PageRank
{
    public static class Map extends MapReduceBase implements Mapper<LongWritable, Text, IntWritable, Text>
    {       
        public void map(LongWritable key,
        				Text value,
        				OutputCollector<IntWritable, Text> output,
        				Reporter reporter
        			   ) throws IOException
        {
        	// '6009554    pr=0.15    [4029274, ... ,5364047]'
            String[] data = value.toString().split("\t");
            
            if (data.length > 2)
            {
            	// vertex, strPR, incident_verteces = line.split('\t')
                IntWritable vertex = new IntWritable(Integer.parseInt(data[0]));
                Double weight = Double.parseDouble(data[1]);
                String struct = data[2].trim();
                
                // print '%s\tG\t%s' % (vertex, incident_verteces)
                output.collect(vertex, new Text("G\t" + struct));
            
                // if len(incident_verteces):
                if (struct.length() > 0)
                {
                	// incident_verteces = list( incident_verteces.split(',') )
                    String[] incident_verteces = struct.split(",");
                    
                    // new_PR = (PR / len(incident_verteces))
                    weight /= incident_verteces.length;
                    for (String v: incident_verteces)
                    {
                    	// print '%s\tW\t%f' % (vertex, new_PR)
                        output.collect(new IntWritable(Integer.parseInt(v)), new Text("W\t" + weight.toString()));
                    }
                    // (len(incident_verteces) == 0)  do not send PR=0
                }
            }
        }
    }
    
    public static class Reduce extends MapReduceBase implements Reducer<IntWritable, Text, IntWritable, Text>
    {  
        private static final double alpha = 0.15;

        public void reduce(IntWritable key, // vertex
        				   Iterator<Text> values,
        				   OutputCollector<IntWritable, Text> output,
        				   Reporter reporter
        				  ) throws IOException
        {
            double weight = 0.;
            String struct = "";
            
            // for v,g in group:
            while( values.hasNext() )
            {
            	// mark, data = g.split('\t')	
        	    String[] data = values.next().toString().split("\t");
        	    
                // mark - weight
        	    // if   mark == 'W': gv.weight += float(data)
                if ( data[0].equals("W") )
                { weight += Double.parseDouble(data[1]); }
                
                // mark - graph structure
                // elif mark == 'G': gv.struct  = data
                else if ( data[0].equals("G") )
                { struct = data[1].trim(); }
                
                // else: raise ValueError
                else throw new IllegalArgumentException();

            }
            // print '%s\tpr=%f\t%s' % (gv.vertex, defPR + (1. - defPR) * gv.weight, gv.struct)
            output.collect(key, new Text(Double.toString(alpha + (1. - alpha) * weight) + "\t" + struct));
        }
    }    
}
