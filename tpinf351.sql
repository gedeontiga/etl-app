CREATE DATABASE IF NOT EXISTS tpinf351;


DROP TABLE IF EXISTS `auteuraffiliation`;
DROP TABLE IF EXISTS `auteurarticle`;
DROP TABLE IF EXISTS `affiliationarticle`;
DROP TABLE IF EXISTS `affiliation`;
DROP TABLE IF EXISTS `article`;
DROP TABLE IF EXISTS `auteur`;

--
-- Table structure for table `continant`
--

DROP TABLE IF EXISTS `continant`;

CREATE TABLE `continant` (
  `idContinant` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idContinant`)
);

LOCK TABLES `continant` WRITE;

INSERT INTO `continant` VALUES (1,'Africa'),(2,'Europe'),(3,'America'),(4,'Asia'),(5,'Oceania');

UNLOCK TABLES;

--
-- Table structure for table `date`
--

DROP TABLE IF EXISTS `date`;

CREATE TABLE `date` (
  `idDate` int(11) NOT NULL AUTO_INCREMENT,
  `annee` varchar(100) NOT NULL,
  PRIMARY KEY (`idDate`)
);


LOCK TABLES `date` WRITE;

INSERT INTO `date` VALUES (1,'2014'),(2,'2015'),(3,'2016'),(4,'2017');

UNLOCK TABLES;

--
-- Table structure for table `affiliation`
--

CREATE TABLE `affiliation` (
  `etablissement` varchar(100) NOT NULL,
  `ville` varchar(100) NOT NULL,
  `pays` varchar(100) NOT NULL,
  `idAffiliation` int(11) NOT NULL AUTO_INCREMENT,
  `idContinant` int(11) DEFAULT NULL,
  PRIMARY KEY (`idAffiliation`),
  KEY `affiliation_continant_FK` (`idContinant`),
  CONSTRAINT `affiliation_continant_FK` FOREIGN KEY (`idContinant`) REFERENCES `continant` (`idContinant`) ON DELETE CASCADE ON UPDATE CASCADE
);


--
-- Table structure for table `article`
--

CREATE TABLE `article` (
  `idArticle` int(11) NOT NULL AUTO_INCREMENT,
  `titre_article` text NOT NULL,
  `idDate` int(50) NOT NULL,
  PRIMARY KEY (`idArticle`),
  KEY `article_date_FK` (`idDate`),
  CONSTRAINT `article_date_FK` FOREIGN KEY (`idDate`) REFERENCES `date` (`idDate`) ON DELETE CASCADE ON UPDATE CASCADE
);

--
-- Table structure for table `auteur`
--

CREATE TABLE `auteur` (
  `idAuteur` int(11) NOT NULL AUTO_INCREMENT,
  `nom_encode` varchar(100) NOT NULL,
  PRIMARY KEY (`idAuteur`)
);

--
-- Table structure for table `auteuraffiliation`
--

CREATE TABLE `auteuraffiliation` (
  `idAuteur` int(11) DEFAULT NULL,
  `idAffiliation` int(11) DEFAULT NULL,
  KEY `auteurFiliation_FK` (`idAffiliation`),
  KEY `auteurFiliation_FK_1` (`idAuteur`),
  CONSTRAINT `auteurFiliation_FK` FOREIGN KEY (`idAffiliation`) REFERENCES `affiliation` (`idAffiliation`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `auteurFiliation_FK_1` FOREIGN KEY (`idAuteur`) REFERENCES `auteur` (`idAuteur`) ON DELETE CASCADE ON UPDATE CASCADE
);

--
-- Table structure for table `auteurarticle`
--

CREATE TABLE `auteurarticle` (
  `idAuteur` int(11) DEFAULT NULL,
  `idArticle` int(11) DEFAULT NULL,
  KEY `AuteurArticle_FK` (`idArticle`),
  KEY `AuteurArticle_FK_1` (`idAuteur`),
  CONSTRAINT `AuteurArticle_FK` FOREIGN KEY (`idArticle`) REFERENCES `article` (`idArticle`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `AuteurArticle_FK_1` FOREIGN KEY (`idAuteur`) REFERENCES `auteur` (`idAuteur`) ON DELETE CASCADE ON UPDATE CASCADE
);

--
-- Table structure for table `affiliationarticle`
--

CREATE TABLE `affiliationarticle` (
  `idArticle` int(11) DEFAULT NULL,
  `idAffiliation` int(11) DEFAULT NULL,
  KEY `affiliationarticle_affiliation_FK` (`idAffiliation`),
  KEY `affiliationarticle_article_FK` (`idArticle`),
  CONSTRAINT `affiliationarticle_affiliation_FK` FOREIGN KEY (`idAffiliation`) REFERENCES `affiliation` (`idAffiliation`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `affiliationarticle_article_FK` FOREIGN KEY (`idArticle`) REFERENCES `article` (`idArticle`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;