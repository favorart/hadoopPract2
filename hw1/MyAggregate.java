import java.io.IOException;
import java.util.Collection;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.ArrayList;
import java.util.Collections;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.FileInputFormat;
import org.apache.hadoop.mapred.FileOutputFormat;
import org.apache.hadoop.mapred.JobClient;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.KeyValueTextInputFormat;
import org.apache.hadoop.mapred.MapReduceBase;
import org.apache.hadoop.mapred.Mapper;
import org.apache.hadoop.mapred.OutputCollector;
import org.apache.hadoop.mapred.Reducer;
import org.apache.hadoop.mapred.Reporter;
import org.apache.hadoop.mapred.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class MyAggregate extends Configured implements Tool
{
    
    public static class MapClass extends MapReduceBase implements Mapper<Text, Text, Text, Text>
    {
        public void map(Text key,
        		        Text value,
                        OutputCollector<Text, Text> output,
                        Reporter reporter
                       ) throws IOException
        {
        	if( key.toString().startsWith("\"") == false )
        	{
	        	String[] split = value.toString().split(",", -1);
	            output.collect(new Text(split[0]), new Text(split[3]));
        	}
        }
    }
    
    public static class Reduce extends MapReduceBase implements Reducer<Text,Text,Text,Text>
    {
    	public void reduce(Text key,
        		           Iterator<Text> values,
                           OutputCollector<Text, Text> output,
                           Reporter reporter
                          ) throws IOException
        {
            // dic = defaultdict(int)
    		Hashtable<Text,Integer> ht = new Hashtable();
            while (values.hasNext())
            {
            	Text country = values.next();
            	if( ht.containsKey(country) )
            	{ ht.put(country, ht.get(country) + 1); }
            	else
            	{ ht.put(country, 1); }
            }

            // sorted_dic = sorted(dic.items(), key=operator.itemgetter(1))
            ArrayList<Integer> arr = new ArrayList<Integer>(ht.values());            
            Collections.sort(arr);
            
            // n = len(dic)
            // count_unique = n                                               #  1  Количество уникальных
            // min  = sorted_dic[ 0][1]                                       #  2  Минимальное значение
            // mid  = sorted_dic[int(n/2)][1]                                 #  3  Медиана
    	    // max  = sorted_dic[-1][1]                                       #  4  Максимальное значение
    	    // mean = (sum(   float(v)  for v in dic.values() ) / n)          #  5  Среднее значение
    	    // devi = (sum( (v-mean)**2 for v in dic.values() ) / n) ** 0.5   #  6  Стандартное откл-нение
            
            Integer count_unique = ht.size();
            Integer min = arr.get(0);
            Integer mid = arr.get(arr.size() / 2);
            Integer max = arr.get(arr.size() - 1);
            Double mean = 0.;
            Double devi	= 0.;
            for(int i=0; i<arr.size(); ++i )
            { mean += arr.get(i); }
            mean /= arr.size();
            
            for(int i=0; i<arr.size(); ++i )
            { devi += (arr.get(i) - mean) * (arr.get(i) - mean); }
            devi /= arr.size();
            devi = Math.pow(devi, 0.5);
            
            // print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (field_i1, count_unique, min, mid, max, mean, devi)
            output.collect(key, new Text(String.format("%s\t%s\t%s\t%s\t%s\t%s", count_unique.toString(), min.toString(), mid.toString(), max.toString(), mean.toString(), devi.toString())) );
        }
    }
    
    public int run(String[] args) throws Exception
    {
        Configuration conf = getConf();
        
        JobConf job = new JobConf(conf, MyAggregate.class);
        
        // System.out.println(args[0], args[1]);

        Path in = new Path(args[0]);
        Path out = new Path(args[1]);
        FileInputFormat.setInputPaths(job, in);
        FileOutputFormat.setOutputPath(job, out);
        
        job.setJobName("MyAggregate");
        job.setMapperClass(MapClass.class);
        job.setReducerClass(Reduce.class);
        
        job.setInputFormat(KeyValueTextInputFormat.class);
        job.setOutputFormat(TextOutputFormat.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);
        job.set("key.value.separator.in.input.line", ",");
        
        JobClient.runJob(job);
        
        return 0;
    }
    
    public static void main(String[] args) throws Exception
    {
        int res = ToolRunner.run(new Configuration(), new MyAggregate(), args);        
        System.exit(res);
    }
}
