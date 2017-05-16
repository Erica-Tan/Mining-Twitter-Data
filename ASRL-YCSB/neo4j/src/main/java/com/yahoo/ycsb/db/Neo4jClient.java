/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you
 * may not use this file except in compliance with the License. You
 * may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied. See the License for the specific language governing
 * permissions and limitations under the License. See accompanying
 * LICENSE file.
 */

/**
 * Neo4j client binding for YCSB.
 *
 *@author Saeed Zareian
 *
 *
 * Submitted  on 7/10/2015.
 *
 */

package com.yahoo.ycsb.db;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.Set;
import java.util.Vector;
import java.util.concurrent.TimeUnit;
import java.io.File;

import org.neo4j.graphdb.Direction;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;
import org.neo4j.graphdb.RelationshipType;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;
import org.neo4j.io.fs.FileUtils;
import org.neo4j.graphdb.schema.IndexDefinition;
import org.neo4j.graphdb.schema.Schema;
import org.neo4j.graphdb.DynamicLabel;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Label;
import org.neo4j.graphdb.ResourceIterator;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.ResourceIterator;

import com.yahoo.ycsb.ByteIterator;
import com.yahoo.ycsb.DB;
import com.yahoo.ycsb.DBException;
import com.yahoo.ycsb.StringByteIterator;

/**
 * Neo4j client for YCSB framework.
 * 
 * 
 * @author Saeed Zareian
 * 
 */
public class Neo4jClient extends DB {


	/**
	 * Initialize any state for this DB. Called once per DB instance; there is one DB instance per client thread.
	 */

	// START SNIPPET: vars
	private static  GraphDatabaseService graphDb= null;
	Node firstNode;
	Node secondNode;
	Relationship relationship;
	// END SNIPPET: vars

	// START SNIPPET: createReltype
	private static enum RelTypes implements RelationshipType
	{
		KNOWS
	}

	private static String DB_PATH = "data.db";
	public void init() throws DBException {
		// initialize Neo4j driver

	synchronized(Neo4jClient.class){
	if(graphDb ==null){
		System.out.println("creating graph db..");
			try {
				FileUtils.deleteRecursively( new File( DB_PATH ) );
			}catch(Exception e) {
				System.out.println(e.getMessage());
				return ;
			}

			// START SNIPPET: startDb
		
			graphDb = new GraphDatabaseFactory().newEmbeddedDatabase(new File(DB_PATH) );
			registerShutdownHook( graphDb );
		
			// END SNIPPET: startDb

			// START SNIPPET: createIndex
			IndexDefinition indexDefinition;
			try 
			{
				Transaction tx = graphDb.beginTx();
				Schema schema = graphDb.schema();
				indexDefinition = schema.indexFor( DynamicLabel.label( "data" ) )
						.on( "key" )
					.create();
				tx.success();
				tx.close();
				tx = graphDb.beginTx();
			// END SNIPPET: createIndex
			// START SNIPPET: wait

		
			schema.awaitIndexOnline( indexDefinition, 20, TimeUnit.SECONDS );
			tx.success();
			tx.close();
			
			}catch(Exception e) {
				e.printStackTrace();
				return ;
			}
			// END SNIPPET: wait
			System.out.println("Neo4j indexes created."); 
		}
		}
	
	}

	@Override
	public void cleanup() throws DBException {
		if (graphDb != null) {
			System.out.println( "Cleaning up ..." );

			
		}
	}

	@Override
	/**
	 * Insert a record in the database. Any field/value pairs in the specified values HashMap will be written into the record with the specified
	 * record key.
	 *
	 * @param table The name of the table
	 * @param key The record key of the record to insert.
	 * @param values A HashMap of field/value pairs to insert in the record
	 * @return Zero on success, a non-zero error code on error. See this class's description for a discussion of error codes.
	 */
	public int insert(String table, String key, HashMap<String, ByteIterator> values) {
		try {

			if(graphDb == null)
				init();
			Transaction tx = graphDb.beginTx();

			Label label = DynamicLabel.label( "data" );

			Node node = graphDb.createNode( label );
			node.setProperty( "key",  key );
			for (Entry<String, String> entry : StringByteIterator.getStringMap(values).entrySet())
				node.setProperty(entry.getKey(), entry.getValue() );
			// START SNIPPET: transaction
			tx.success();


			return 0;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return 1;
	}

	@Override
	/**
	 * Delete a record from the database.
	 *
	 * @param table The name of the table
	 * @param key The record key of the record to delete.
	 * @return Zero on success, a non-zero error code on error. See this class's description for a discussion of error codes.
	 */
	public int delete(String table, String key) {
		
		 try 
         {
			 Transaction tx = graphDb.beginTx();
             Label label = DynamicLabel.label( "data" );
             String idToFind = key;
             String nameToFind = key;
             ResourceIterator<Node> it= graphDb.findNodes( label, "key", nameToFind ) ;
             while ( it.hasNext() )
             {
             	Node node= it.next();
                 node.delete();
             }
             tx.success();
         }catch(Exception e) {
        	 e.printStackTrace();	
         }
		return 1;
	}

	@Override
	/**
	 * Read a record from the database. Each field/value pair from the result will be stored in a HashMap.
	 *
	 * @param table The name of the table
	 * @param key The record key of the record to read.
	 * @param fields The list of fields to read, or null for all of them
	 * @param result A HashMap of field/value pairs for the result
	 * @return Zero on success, a non-zero error code on error or "not found".
	 */
	public int read(String table, String key, Set<String> fields, HashMap<String, ByteIterator> result) {
		
			 // START SNIPPET: find nodes
            Label label = DynamicLabel.label( "data" );
            String idToFind = key;
            String nameToFind = key;
            try 
            {
            	 Transaction tx = graphDb.beginTx();
               
                	ResourceIterator<Node> it =
                            graphDb.findNodes( label, "key", nameToFind );
                    ArrayList<Node> Nodes = new ArrayList<Node>();
                    while ( it.hasNext() )
                    {
                    	Nodes.add( it.next() );
                    }
                //    System.out.println(Nodes.size()+" nodes found");
                    for ( Node node : Nodes )
                    {
                        //System.out.println( "The key of node " + idToFind + " is " + node.getProperty( "key" ) );
                    }
           
			
		} catch (Exception e) {
			e.printStackTrace();
		}
		return 1;
	}

	@Override
	/**
	 * Update a record in the database. Any field/value pairs in the specified values HashMap will be written into the record with the specified
	 * record key, overwriting any existing values with the same field name.
	 *
	 * @param table The name of the table
	 * @param key The record key of the record to write.
	 * @param values A HashMap of field/value pairs to update in the record
	 * @return Zero on success, a non-zero error code on error. See this class's description for a discussion of error codes.
	 */
	public int update(String table, String key, HashMap<String, ByteIterator> values) {
		
		  // START SNIPPET: updateUsers
        try 
        {
        	Transaction tx = graphDb.beginTx();
            Label label = DynamicLabel.label( "data" );
            String idToFind = key;
            String nameToFind = key;
            ResourceIterator<Node> it= graphDb.findNodes( label, "key", nameToFind ) ;
            while ( it.hasNext() )
            {
            	Node node= it.next();
            	 for (Entry<String, String> entry : StringByteIterator.getStringMap(values).entrySet())            	
            		 node.setProperty( entry.getKey(), entry.getValue());
            }
            tx.success();
        }catch(Exception e) {
        	e.printStackTrace();
        }
		return 1;
	}

	@Override
	/**
	 * Perform a range scan for a set of records in the database. Each field/value pair from the result will be stored in a HashMap.
	 *
	 * @param table The name of the table
	 * @param startkey The record key of the first record to read.
	 * @param recordcount The number of records to read
	 * @param fields The list of fields to read, or null for all of them
	 * @param result A Vector of HashMaps, where each HashMap is a set field/value pairs for one record
	 * @return Zero on success, a non-zero error code on error. See this class's description for a discussion of error codes.
	 */
	public int scan(String table, String startkey, int recordcount, Set<String> fields, Vector<HashMap<String, ByteIterator>> result) {
		try {
		
			return 0;
		} catch (Exception e) {
			e.printStackTrace();
		}
		return 1;
	}
	private static void registerShutdownHook( final GraphDatabaseService graphDb )
	{
		// Registers a shutdown hook for the Neo4j instance so that it
		// shuts down nicely when the VM exits (even if you "Ctrl-C" the
		// running application).
		Runtime.getRuntime().addShutdownHook( new Thread()
		{
			@Override
			public void run()
			{
				try {
					graphDb.shutdown();
				}catch (Exception e) {
					e.printStackTrace();
				}
			}
		} );
	}
}
