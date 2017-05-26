echo "neo4j YCSB Workload Generator"


SET NUMBER_OF_OPERATIONS=75000
set TARGETS=1000,2000,3000,4000,5000,6000,7000,8000,9000,10000


rem SET NUMBER_OF_OPERATIONS=1000000

rem set TARGETS=1000,2000,4000,8000,16000,32000,64000,128000,256000,512000

set NUMBER_OF_THREADS=1,2,5,10,25,50,100,200,500,1000



SET WORKLOAD_TYPE=a

FOR %%a in (%TARGETS%) do (
  FOR %%b in (%NUMBER_OF_THREADS% %%a) DO (

    echo "Loading workload "%WORKLOAD_TYPE%"......."

    python ../bin/ycsb load neo4j -s -P workloads/workload%WORKLOAD_TYPE%  -p recordcount=%NUMBER_OF_OPERATIONS% -threads %%b > logs/outputLoada%%a_%%b_%WORKLOAD_TYPE%.txt

    echo "Finished loading workload "%WORKLOAD_TYPE%""

    echo "EXECUTING WORKLOAD "%WORKLOAD_TYPE%"......"


    python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %%b -target %%a > logs/neo4jrun%%a_%%b_%WORKLOAD_TYPE%.out

	  TIMEOUT 20


    echo "FINISHED WORKLOAD "%WORKLOAD_TYPE%"......"
  )
)


SET WORKLOAD_TYPE=c

FOR %%a in (%TARGETS%) do (
  FOR %%b in (%NUMBER_OF_THREADS% %%a) DO (

    echo "Loading workload "%WORKLOAD_TYPE%"......."

    python ../bin/ycsb load neo4j -s -P workloads/workload%WORKLOAD_TYPE%  -p recordcount=%NUMBER_OF_OPERATIONS% -threads %%b > logs/outputLoada%%a_%%b_%WORKLOAD_TYPE%.txt

    echo "Finished loading workload "%WORKLOAD_TYPE%""

    echo "EXECUTING WORKLOAD "%WORKLOAD_TYPE%"......"


    python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %%b -target %%a > logs/neo4jrun%%a_%%b_%WORKLOAD_TYPE%.out

    TIMEOUT 20


    echo "FINISHED WORKLOAD "%WORKLOAD_TYPE%"......"
  )
)


SET WORKLOAD_TYPE=g

FOR %%a in (%TARGETS%) do (
  FOR %%b in (%NUMBER_OF_THREADS% %%a) DO (

    echo "Loading workload "%WORKLOAD_TYPE%"......."

    python ../bin/ycsb load neo4j -s -P workloads/workload%WORKLOAD_TYPE%  -p recordcount=%NUMBER_OF_OPERATIONS% -threads %%b > logs/outputLoada%%a_%%b_%WORKLOAD_TYPE%.txt

    echo "Finished loading workload "%WORKLOAD_TYPE%""

    echo "EXECUTING WORKLOAD "%WORKLOAD_TYPE%"......"


    python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %%b -target %%a > logs/neo4jrun%%a_%%b_%WORKLOAD_TYPE%.out

    TIMEOUT 20


    echo "FINISHED WORKLOAD "%WORKLOAD_TYPE%"......"
  )
)
