-- MySQL dump 10.13  Distrib 5.5.32, for Linux (x86_64)
--
-- Host: localhost    Database: web
-- ------------------------------------------------------
-- Server version	5.5.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `description`
--

DROP TABLE IF EXISTS `description`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `description` (
  `id` int(11) NOT NULL,
  `description` varchar(3000) DEFAULT NULL,
  `recurrence` varchar(200) DEFAULT NULL,
  `dimension_x` int(11) DEFAULT NULL,
  `dimension_y` int(11) DEFAULT NULL,
  `solutiontext` varchar(2000) DEFAULT NULL,
  `constants` varchar(200) DEFAULT NULL,
  `arrays` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `description_ibfk_1` FOREIGN KEY (`id`) REFERENCES `problem` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `description`
--

LOCK TABLES `description` WRITE;
/*!40000 ALTER TABLE `description` DISABLE KEYS */;
INSERT INTO `description` VALUES (1,'Given a set of items, where item i has mass m<sub>i</sub> and  value v<sub>i</sub>, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit C and the total value is as large as possible.','default=0\nT[0]=0\nT[i]=max(T[i-weights[j]]+values[j]) for i in 1:C+1 where weights[j]<=i',10,1,'The integer knapsack problem is a 1D dynamic programming problem. We have a table where T[i] holds the optimal value which can be obtained for a knapsack with capacity i. Obviously T[0]=0. We then define T[C]= max(v[i]+T[C-w[i]]) where we iterate over all items with weights less than or equal to C','[(\'C\',10)]','[(\'weights\',10,10),(\'values\',10,10)]'),(6,'Output the first N numbers','T[0]=1\nT[i]=T[i-1]+1 for i in 1:N',0,1,'Obvious','[(\'N\',15)]',NULL),(7,'Find the maximal value in the array','T[0]=values[0]\nT[i]=max(T[i-1],values[i]) for i in 1:n',10,1,'Obvious',NULL,'[(\'values\',10,20)]'),(8,'Give the first N terms of the Fibonacci sequence.','T[0]=1\nT[1]=1\nT[i]=T[i-1]+T[i-2] for i in 2:N',10,1,'Obvious','[(\'N\',15)]',NULL),(9,'Find the maximum value contiguous subsequence','T[0]=values[0]\nT[i]=max(T[i-1]+values[i],values[i]) for i in 1:n',10,1,'...',NULL,'[(\'values\',10,10)]'),(10,'Making change','T[0]=0\nT[i]= min(T[i-values[j]]+1) for i in 1:C where values[j]<=i',10,1,'...','[(\'C\',15)]','[(\'values\',10,10)]'),(11,'Find the Longest Increasing subsequence','default=1\nT[0]=1\nT[i]=max(T[j]+1) for i in 1:n where j<i and values[j]<values[i]',10,1,'...',NULL,'[(\'values\',10,10)]'),(12,'Minimum number of changes...','T[0][i]=i for i in 0:n+1\nT[i][0]=i for i in 0:n+1\nT[i][j]=min(T[i-1][j]+1,T[i][j-1]+1,T[i-1][j-1]+(word1[i-1]!=word2[j-1])) for i in 1:n+1 for j in 1:n+1',10,10,'xaxa','[]','[(\'word1\',5,5),(\'word2\',5,5)]'),(13,'Integer Knapsack without Repetitions','T[0][i]= 0 for i in 0:C+1\nT[i][j]=max(T[i-1][j],T[i-1][j-weights[i-1]]+values[i-1]) for i in 1:n for j in 0:C+1',10,10,'xx','[(\'C\',10)]','[(\'weights\',10,10),(\'values\',10,10)]');
/*!40000 ALTER TABLE `description` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `example_users`
--

DROP TABLE IF EXISTS `example_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `example_users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(80) NOT NULL,
  `passw` varchar(40) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `privilege` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `example_users`
--

LOCK TABLES `example_users` WRITE;
/*!40000 ALTER TABLE `example_users` DISABLE KEYS */;
INSERT INTO `example_users` VALUES (1,'mboy','xaxa','mboy@gmail.com',1),(2,'goko','xaxa','fsa@gags',0),(3,'goko','483b855715a28b47217a74927601a416','fsa@gags',0),(4,'goko','483b855715a28b47217a74927601a416','fsa@gags',0),(5,'marty','5669dc348737ddda620bd0dd966f60f9','f@g',0),(6,'jojo','483b855715a28b47217a74927601a416','m@g',0),(7,'kolyo','483b855715a28b47217a74927601a416','ko@f',0),(8,'alek','cc96c3f112775b6b0c8a083f863d3660','ff@fgsafp',0),(9,'john','483b855715a28b47217a74927601a416','fa@gg',0),(10,'john','483b855715a28b47217a74927601a416','fs@gg',0),(11,'koko','483b855715a28b47217a74927601a416','fs@gs',0),(12,'user','483b855715a28b47217a74927601a416','trq@gas',0),(13,'veso','811584043b844704c9bb9a6e99dd05d3','gsaga@gagas',0);
/*!40000 ALTER TABLE `example_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `problem`
--

DROP TABLE IF EXISTS `problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problem` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `difficulty` int(11) NOT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problem`
--

LOCK TABLES `problem` WRITE;
/*!40000 ALTER TABLE `problem` DISABLE KEYS */;
INSERT INTO `problem` VALUES (1,'test',1,1),(2,'test1',1,1),(3,'test2',2,2),(4,'test3',3,3),(5,'test3',4,4),(6,'Numbers',1,1),(7,'Maximal Value',1,1),(8,'Fibonacci',1,1),(9,'Maximum Value Contiguous Subsequence',1,1),(10,'Making Change',1,1),(11,'Longest Increasing Subsequence',1,1),(12,'Edit Distance',1,1),(13,'Integer Knapsack without Repetitions',1,1);
/*!40000 ALTER TABLE `problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sessions`
--

DROP TABLE IF EXISTS `sessions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sessions` (
  `session_id` char(128) NOT NULL,
  `atime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `data` text,
  UNIQUE KEY `session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sessions`
--

LOCK TABLES `sessions` WRITE;
/*!40000 ALTER TABLE `sessions` DISABLE KEYS */;
INSERT INTO `sessions` VALUES ('506f104ca0d015ef4496ea6aa203b8cec446cf62','2013-11-11 02:06:27','KGRwMQpTJ2lwJwpwMgpWMjUuMTQuMTA2LjQxCnAzCnNTJ3NvbHV0aW9uaW5kZXgnCnA0CkkwCnNT\nJ2lkcCcKcDUKSS0xCnNTJ2luc3RhbmNlJwpwNgoobHA3ClMnYScKYXNTJ3Nlc3Npb25faWQnCnA4\nClMnNTA2ZjEwNGNhMGQwMTVlZjQ0OTZlYTZhYTIwM2I4Y2VjNDQ2Y2Y2MicKcDkKc1MncHJvYmxl\nbXN0YXR1cycKcDEwCkktMQpzUydwcml2aWxlZ2UnCnAxMQpJMApzUydsb2dpbicKcDEyCkkwCnNT\nJ3VzZXInCnAxMwpTJycKcy4=\n'),('54bc29a5717deedad2419acf08472773bee2f3de','2013-11-11 02:11:01','KGRwMQpTJ2lwJwpwMgpWMjUuMTYuMTU1LjcKcDMKc1Mnc29sdXRpb25pbmRleCcKcDQKSTAKc1Mn\naWRwJwpwNQpWMTMKcDYKc1MnaW5zdGFuY2UnCnA3CihpcHJvYmxlbQpwcm9ibGVtCnA4CihkcDkK\nUydjb250ZW50JwpwMTAKVjxwPkludGVnZXIgS25hcHNhY2sgd2l0aG91dCBSZXBldGl0aW9ucwpw\nMTEKc1Mnc29sdXRpb24nCnAxMgpWeHgKcDEzCnNTJ2NvbnN0YW50cycKcDE0CihkcDE1ClMnQycK\nSTkKc3NTJ2xpc3RzJwpwMTYKKGRwMTcKUyd2YWx1ZXMnCnAxOAoobHAxOQpJNQphSTYKYUkzCmFJ\nNgphSTEwCmFJMQphSTMKYUk3CmFJNQphSTkKYXNTJ3dlaWdodHMnCnAyMAoobHAyMQpJOQphSTIK\nYUk0CmFJNwphSTIKYUk1CmFJMwphSTUKYUk5CmFJMwphc3NTJ2RpbWVuc2lvbnMnCnAyMgooTDEw\nTApJMTEKdHAyMwpzYnNTJ3Nlc3Npb25faWQnCnAyNApTJzU0YmMyOWE1NzE3ZGVlZGFkMjQxOWFj\nZjA4NDcyNzczYmVlMmYzZGUnCnAyNQpzUydwcm9ibGVtc3RhdHVzJwpwMjYKSTEKc1MncHJpdmls\nZWdlJwpwMjcKSTAKc1MnbG9naW4nCnAyOApJMApzUyd1c2VyJwpwMjkKUycnCnMu\n'),('570a5e2bae0178d3f358019be091eefedf3ca395','2013-11-11 02:07:17','KGRwMQpTJ2lwJwpwMgpWMTkyLjE2OC4xLjUKcDMKc1Mnc29sdXRpb25pbmRleCcKcDQKSTAKc1Mn\naWRwJwpwNQpJLTEKc1MnaW5zdGFuY2UnCnA2CihscDcKUydhJwphc1Mnc2Vzc2lvbl9pZCcKcDgK\nUyc1NzBhNWUyYmFlMDE3OGQzZjM1ODAxOWJlMDkxZWVmZWRmM2NhMzk1JwpwOQpzUydwcm9ibGVt\nc3RhdHVzJwpwMTAKSS0xCnNTJ3ByaXZpbGVnZScKcDExCkkwCnNTJ2xvZ2luJwpwMTIKSTAKc1Mn\ndXNlcicKcDEzClMnJwpzLg==\n'),('58388f373174c301749ca432464c4984509e59ab','2013-11-11 18:02:52','KGRwMQpTJ2lwJwpwMgpWMTI3LjAuMC4xCnAzCnNTJ3NvbHV0aW9uaW5kZXgnCnA0CkkwCnNTJ2lk\ncCcKcDUKVjgKc1MnaW5zdGFuY2UnCnA2CihpcHJvYmxlbQpwcm9ibGVtCnA3CihkcDgKUydjb250\nZW50JwpwOQpWPHA+R2l2ZSB0aGUgZmlyc3QgTiB0ZXJtcyBvZiB0aGUgRmlib25hY2NpIHNlcXVl\nbmNlLgpwMTAKc1Mnc29sdXRpb24nCnAxMQpWT2J2aW91cwpwMTIKc1MnY29uc3RhbnRzJwpwMTMK\nKGRwMTQKUydOJwpJMTUKc3NTJ2xpc3RzJwpwMTUKKGRwMTYKc1MnZGltZW5zaW9ucycKcDE3CihM\nMUwKSTExCnRwMTgKc2JzUydzZXNzaW9uX2lkJwpwMTkKUyc1ODM4OGYzNzMxNzRjMzAxNzQ5Y2E0\nMzI0NjRjNDk4NDUwOWU1OWFiJwpwMjAKc1MncHJvYmxlbXN0YXR1cycKcDIxCkkxCnNTJ3ByaXZp\nbGVnZScKcDIyCkkwCnNTJ2xvZ2luJwpwMjMKSTAKc1MndXNlcicKcDI0ClMnJwpzLg==\n'),('fddde2e0a32178b0be65a55e9067d2d68a0b4905','2013-11-11 01:45:25','KGRwMQpTJ2lwJwpwMgpWMTI3LjAuMC4xCnAzCnNTJ3NvbHV0aW9uaW5kZXgnCnA0CkkwCnNTJ2lk\ncCcKcDUKSS0xCnNTJ2luc3RhbmNlJwpwNgoobHA3ClMnYScKYXNTJ3Nlc3Npb25faWQnCnA4ClMn\nZmRkZGUyZTBhMzIxNzhiMGJlNjVhNTVlOTA2N2QyZDY4YTBiNDkwNScKcDkKc1MncHJvYmxlbXN0\nYXR1cycKcDEwCkktMQpzUydwcml2aWxlZ2UnCnAxMQpJMApzUydsb2dpbicKcDEyCkkwCnNTJ3Vz\nZXInCnAxMwpTJycKcy4=\n');
/*!40000 ALTER TABLE `sessions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `todo`
--

DROP TABLE IF EXISTS `todo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `todo` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `title` text,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `done` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `todo`
--

LOCK TABLES `todo` WRITE;
/*!40000 ALTER TABLE `todo` DISABLE KEYS */;
INSERT INTO `todo` VALUES (1,'Learn web.py','2013-09-30 16:02:03',0);
/*!40000 ALTER TABLE `todo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-11-12  2:05:29
