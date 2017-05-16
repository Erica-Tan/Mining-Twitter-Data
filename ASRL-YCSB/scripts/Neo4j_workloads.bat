echo "neo4j YCSB Workload Generator"

SET NUMBER_OF_OPERATIONS=75000
SET NUMBER_OF_THREADS=10
SET TARGET_1=1000
SET TARGET_2=2000
SET TARGET_3=3000
SET TARGET_4=4000
SET TARGET_5=5000
SET TARGET_6=6000
SET TARGET_7=7000
SET TARGET_8=8000
SET TARGET_9=9000
SET TARGET_10=10000



SET WORKLOAD_TYPE=a

echo "Loading workload "%WORKLOAD_TYPE%"......."

python ../bin/ycsb load neo4j -s -P workloads/workload%WORKLOAD_TYPE%  -p recordcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% > logs/outputLoada.txt

echo "Finished loading workload "%WORKLOAD_TYPE%""

echo "EXECUTING WORKLOAD "%WORKLOAD_TYPE%"......"


python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_1% > logs/neo4jrun%TARGET_1%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_2% > logs/neo4jrun%TARGET_2%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_3% > logs/neo4jrun%TARGET_3%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_4% > logs/neo4jrun%TARGET_4%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_6% > logs/neo4jrun%TARGET_6%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_7% > logs/neo4jrun%TARGET_7%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_8% > logs/neo4jrun%TARGET_8%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_5% > logs/neo4jrun%TARGET_5%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_9% > logs/neo4jrun%TARGET_9%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

TIMEOUT 20
python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_10% > logs/neo4jrun%TARGET_10%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out




echo "FINISHED WORKLOAD "%WORKLOAD_TYPE%"......"







rem SET WORKLOAD_TYPE=b

rem echo "Loading workload "%WORKLOAD_TYPE%"......."

rem python ../bin/ycsb load neo4j -s -P workloads/workload%WORKLOAD_TYPE%  -p recordcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% > logs/outputLoada.txt


rem TIMEOUT 20

rem echo "Finished loading workload "%WORKLOAD_TYPE%""

rem echo "EXECUTING WORKLOAD "%WORKLOAD_TYPE%"......"


rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_1% > logs/neo4jrun%TARGET_1%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_2% > logs/neo4jrun%TARGET_2%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_3% > logs/neo4jrun%TARGET_3%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_4% > logs/neo4jrun%TARGET_4%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_6% > logs/neo4jrun%TARGET_6%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_7% > logs/neo4jrun%TARGET_7%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_8% > logs/neo4jrun%TARGET_8%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_5% > logs/neo4jrun%TARGET_5%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_9% > logs/neo4jrun%TARGET_9%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out

rem TIMEOUT 20
rem python ../bin/ycsb run neo4j -s -P workloads/workload%WORKLOAD_TYPE% -p operationcount=%NUMBER_OF_OPERATIONS% -threads %NUMBER_OF_THREADS% -target %TARGET_10% > logs/neo4jrun%TARGET_10%_%NUMBER_OF_THREADS%_%WORKLOAD_TYPE%.out




rem echo "FINISHED WORKLOAD "%WORKLOAD_TYPE%"......"