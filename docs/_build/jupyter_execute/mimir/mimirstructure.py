# MIMIR database structure and setup

## Background
The database, associated R shiny interface and introduction to MIMIR were developed by Shu En Lim with subsequent modification and tweaking by Craig Syms.  

**MIMIR**, named after the Norse god of knowledge and wisdom, is SNTech's data analysis tool for bycatch reduction. MIMIR aims to consolidate data across the fishing sector to enable fisheries to make better decisions especially in gear selection and placement of bycatch reduction devices. Why? Potentially useful data is scattered amongst journal articles, logbooks and images that are difficult or expensive to access, particularly for users outside the field. Another challenge is in bridging together knowledge from diverse sectors including biology, engineering and business. This version is a database of past scientific trials using light as a bycatch reduction tool, and visual physiology measurements of species from interest (Dr Sara Mynott).

## Structure
The database is comprised of four tables in a relational database (RDBMS). This will eventually be stored on a MySQL database on SNTech's virtual server.  

The general organisation is:

```{figure} mimirtablestructure.png
```

**PK** refers to a data field's designation as a Primary Key.  
Note also the links between Primary keys of the different tables. You will see this in the CREATE TABLE statements below in the REFERENCES table(key) syntax. This does the hierarchical linking of tables with each other.

## Generating the database
The easiest way to repeatably generate a database *de novo* is by coding it directly using SQL. It is possible to use a graphical interface such as [phpMyAdmin](https://www.phpmyadmin.net/), but click and point interfaces are prone to (human) errors.  

**The procedure is:**
1. **Secure shell into the Ionos server** 
2. **Log into MySQL**  

```{warning}
This will change when I set the MySQL permissions. Using root login is dangerous!
```

In the command window  

```
mysql -u root -p  
```

This will bring up the MySQL cursor. 

3. Now we run the code:

```sql
#MYSQL MIMIR DATABASE
#MAINTAINER: CRAIG SYMS, CRAIG@SNTECH.CO.UK
#ORIGINAL CODE: SHU EN LIM

CREATE DATABASE mimir;

SHOW DATABASES;

USE mimir

CREATE TABLE fishes(
    species_id serial PRIMARY KEY,
    genus_name varchar(30) NOT NULL,
    species_name varchar(30) NOT NULL,
    common_name varchar(30) NOT NULL,
    category varchar(30) NOT NULL
    );

CREATE TABLE trials(
    trial_id serial PRIMARY KEY,
    trial_year smallint NOT NULL,
    country varchar(30) NOT NULL,
    locality varchar(30) NOT NULL,
    source text NOT NULL,
    first_author varchar(30) NOT NULL,
    contact_author varchar(100),
    notes text
    );

CREATE TABLE experiments(
    experiment_id serial PRIMARY KEY,
    trial_id integer NOT NULL REFERENCES trials(trial_id),
    geog POINT NOT NULL,
    exp_type varchar(10) NOT NULL,
    gear_type varchar(30) NOT NULL,
    gear_modification varchar(40) NOT NULL,
    light_source varchar(30) NOT NULL,
    light_manufacturer varchar(50) NOT NULL,	
    light_source_location varchar(300) NOT NULL,
    num_light_sources smallint,
    time_of_day varchar(10),
    deployment_depth_start smallint,
    deployment_depth_end smallint,
    exp_date_start DATE,
    exp_date_end DATE
    );

CREATE TABLE results(
    result_id serial PRIMARY KEY,
    experiment_id integer NOT NULL REFERENCES experiments(experiment_id),
    trial_id integer NOT NULL REFERENCES trials(trial_id),
    species_id integer NOT NULL REFERENCES fishes(species_id),
    catch_type varchar(10),
    colour_name varchar(10) NOT NULL,
    colour_wavelength smallint NOT NULL,
    colour_wavelength_end smallint,
    response boolean,
    response_type varchar(20)
    );
```

We have now generated an empty database. Currently, there are only experiments from 12 studies, so it is expedient to enter them directly using SQL code:

```sql
INSERT INTO fishes VALUES
    (1,'Gadus','morhua','cod','roundfish'),
    (2,'Melanogrammus','aeglefinus','haddock','roundfish'),
    (3,'Merlangius','merlangus','whiting','roundfish'),
    (4,'Pandalus','borealis','deepwater shrimp','crustacean'),
    (5,'Hippoglossoides','platessoides','american plaice','flatfish'),
    (6,'Meganyctiphanes','norvegica','northern krill','crustacean'),
    (7,'Limanda','limanda','common dab','flatfish'),
    (8,'Pleuronectes','platessa','european plaice','flatfish'),
    (9,'Nephrops','norvegicus','norway lobster','crustacean'),
    (10,'Aequipecten','opercularis','queen scallop','mollusk'),
    (11,'Microstomus','kitt','lemon sole','flatfish'),
    (12,'Merluccius','merluccius','european hake','roundfish'),
    (13,'Micromesistius','poutassou','blue whiting','roundfish'),
    (14,'Trachurus','trachurus','horse mackerel','roundfish'),
    (15,'Thysanoessa','inermis','krill','crustacean'),
    (16,'Chionoecetes','opilio','snow crab','crustacean'),
    (17,'Oncorhynchus','tshawytscha','chinook salmon', 'roundfish');

INSERT INTO trials VALUES
    (1,2018,'Norway','Barents Sea','10.1016/j.fishres.2018.03.023','Larsen','roger.larsen@uit.no',NULL),
    (2,2018,'Norway','Langenuen','10.1371/journal.pone.0190918','Utne-Palm','annecu@imr.no',NULL),
    (3,2017,'Norway','Barents Sea','10.1139/cjfas-2017-0002','Grimaldo','eduardo.grimaldo@sintef.no',NULL),
    (4,2019,'Scotland','Orkney Islands','10.1016/j.fishres.2019.03.010','ONeill', 'barone@aqua.dtu.dk',NULL),
    (5,2020,'Isle of Man','Isle of Man territorial sea','10.1017/S0025315420000028','Southworth','lucy.k.southworth@gmail.com',NULL),
    (6,2018,'Denmark','Skagerrak','10.1093/icesjms/fsy048','Melli','vmel@aqua.dtu.dk','check paper for length distribution notes'),
    (7,2014,'Sweden','Baltic Sea','10.1016/j.fishres.2014.04.012','Bryhn','andreas.bryhn@slu.se','check paper for number of pots per experiment'),
    (8,2020,'Spain','Bay of Biscay','10.3989/scimar.04975.17A','Cuende','elsacuende@gmail.com','LEDs did not significantly affect the SMP’s release efficiency for any species. Increasing panel size had a significant positive effect on blue whiting, and placing the SMP in the lower panel improved hake.'),
    (9,2019,'Spain','Bay of Biscay','10.1016/j.fishres.2019.105431','Cuende','elsacuende@gmail.com',NULL),
    (10,2018,'Norway','Ramfjord','10.1093/icesjms/fsy099','Humborstad','oddb@hi.no',NULL),
    (11,2017,'Canada','Newfoundland and Labrador','10.1016/j.aaf.2017.05.001','Nguyen','khanh.nguyen@mi.mun.ca',NULL),
    (12,2019,'United States','Oregon','10.1016/j.fishres.2019.04.013','Lomeli','mlomeli@psmfc.org',NULL);

INSERT INTO experiments VALUES
    (1,1,GeomFromText('POINT(30.167 75.500)'),'sea','bottom trawl','nordmore grid','LED','Lindgren-Pitman Electralume','lower part of grid pointing in towing direction and downwards',4,'twilight',363,381,'2016-11-19','2016-11-22'),
    (2,2,GeomFromText('POINT(5.517 60.050)'),'lab','tank','none','LED','unknown','right wall',12,NULL,0,NULL,'2016-02-01','2016-03-31'),
    (3,3,GeomFromText('POINT(30.133 70.483)'),'sea','bottom trawl','square mesh panel','LED','Lindgren-Pitman Electralume','4 at centre of square mesh and 4 attached to selvedges',8,'daytime',46,410,'2016-02-29','2016-03-09'),	
    (4,4,GeomFromText('POINT(-3.000 59.000)'),'sea','demersal prawn trawl','separator panel','LED lightline','PhotoSynergy Ltd PSL5000','leading edge of separator panel',15,'daytime',75,85,'2014-09-01','2014-09-30'),
    (5,4,GeomFromText('POINT(-3.000 59.000)'),'sea','demersal prawn trawl','separator panel','LED lightline','PhotoSynergy Ltd PSL5000','leading edge of separator panel at reduced height and centre section of fishing line',15,'nighttime',75,85,'2015-03-01','2015-03-31'),
    (6,5,GeomFromText('POINT(-4.400 54.200)'),'sea','otter trawl','square mesh panel','LED','SafetyNet Technologies','attached to square mesh panel as 2x3',6,'daytime',29,40,'2017-06-01','2017-08-31'),
    (7,5,GeomFromText('POINT(-5.000 54.000)'),'sea','otter trawl','square mesh panel','LED','SafetyNet Technologies','attached to square mesh panel as 2x3',6,'daytime',45,90,'2017-06-01','2017-08-31'),
    (8,6,GeomFromText('POINT(9.932 58.352)'),'sea','combi trawl','none','LED','Lindgren-Pitman Electralume','lower netting panel in aft part of tapered section',10,'both',45,86,'2016-09-05','2016-09-29'),
    (9,6,GeomFromText('POINT(9.932 58.352)'),'sea','combi trawl','none','LED','Lindgren-Pitman Electralume','upper netting panel in aft part of tapered section',10,'both',45,86,'2016-09-05','2016-09-29'),
    (10,7,GeomFromText('POINT(15.320 56.045)'),'sea','pot','square mesh panel','LED','Artisan Fisheries','by the bait bag inthe middle of the pot',2,'both',20,20,'2009-04-01','2010-07-31'),
    (11,7,GeomFromText('POINT(14.900 55.800)'),'sea','pot','square mesh panel','LED','Artisan Fisheries','by the bait bag inthe middle of the pot',2,'both',43,43,'2010-06-01','2010-11-30'),
    (12,8,GeomFromText('POINT(-1.650 43.800)'),'sea','bottom trawl','square mesh panel','LED','unknown','upper panel of extension piece near SMP',10,'daylight',108,122,'2018-06-01','2018-06-15'),
    (13,8,GeomFromText('POINT(-1.650 43.800)'),'sea','bottom trawl','square mesh panel','LED','unknown','lower panel of extension piece opposite SMP',10,'daylight',108,122,'2018-06-01','2018-06-15'),
    (14,9,GeomFromText('POINT(-2.205 43.400)'),'sea','bottom trawl','square mesh panel','LED','CENTRO Power Light SW2','over the SMP to attract fish towards the panel and increase contact probability',10,NULL,106,128,'2017-06-08','2017-06-19'),	
    (15,10,GeomFromText('POINT(19.347 69.323)'),'sea','pot','none','LED','Artisan Fisheries','by the bait bag inthe middle of the pot',1,'nighttime',120,124,'2016-09-01','2016-09-30'),
    (16,10,GeomFromText('POINT(19.347 69.323)'),'sea','pot','none','LED','Brinyte DIV01','hanging centrally from the roof in the upper chamber of the pot pointing towards the bait bag',1,'nighttime',120,124,'2016-09-01','2016-09-30'),
    (17,11,GeomFromText('POINT(-52.679 47.588)'),'lab','tank','none','LED','Lindgren-Pitman Electralume','suspended at the end of the pool tank in a vertically oriented 64 mm diameter black PVC tube to limit light emitted. The light aligned with a 22 mm diameter hole that was 20 cm from the tank floor to create a small focused light pattern with the source approximately 2.3 m from the cage',1,NULL,0,NULL,'2016-01-28','2016-02-19'),
    (18,11,GeomFromText('POINT(-52.200 47.200)'),'sea','trap','none','LED','Lindgren-Pitman Electralume','inside trap with 453 g of mixed squid and herring in a perforated plastic jar',1,'both',165,173,'2016-04-26','2016-05-23'),
    (19,11,GeomFromText('POINT(-48.000 46.000)'),'sea','trap','none','LED','Lindgren-Pitman Electralume','inside trap with no bait',1,'both',80,300,'2016-05-01','2016-06-30'),
    (20,12,GeomFromText('POINT(-124.370 44.195)'),'sea','midwater trawl','square mesh ramp to escape window','LED', 'Lindgren-Pitman Electralume','illuminating specific windows: 8 LED clusters along a forward escape window or 6 LED clusters along an aft escape window',6,'daytime',135,195,'2015-09-01','2015-09-30'),
    (21,12,GeomFromText('POINT(-124.290 44.350)'),'sea','midwater trawl','square mesh ramp to escape window','LED', 'Lindgren-Pitman Electralume','all windows: 7 LED clusters on each forward escape window and 5 LED clusters on each aft escape window',5,'daytime',135,195,'2017-05-01','2017-11-30');

INSERT INTO results VALUES
    (1,1,1,1,'bycatch','green',519,NULL,FALSE,'negligible'),
    (2,1,1,2,'bycatch','green',519,NULL,FALSE,'negligible'),
    (3,1,1,5,'bycatch','green',519,NULL,FALSE,'negligible'),
    (4,1,1,4,'target','green',519,NULL,FALSE,'negligible'),
    (5,2,2,6,'target','green',448,560,TRUE,'towards'),
    (6,2,2,6,'target','white',425,750,TRUE,'towards'),
    (7,2,2,1,'target','blue',448,NULL,FALSE,'negligible'),
    (8,2,2,1,'target','green',505,NULL,FALSE,'negligible'),
    (9,2,2,1,'target','green',530,NULL,FALSE,'negligible'),
    (10,2,2,1,'target','white',425,750,FALSE,'negligible'),
    (11,3,3,1,'bycatch','green',519,NULL,FALSE,'negligible'),
    (12,3,3,2,'bycatch','green',519,NULL,TRUE,'erratic escape'),
    (13,4,4,2,NULL,'green',530,NULL,FALSE,'negligible'),
    (14,4,4,1,NULL,'green',530,NULL,FALSE,'negligible'),
    (15,4,4,7,NULL,'green',530,NULL,TRUE,'towards seabed'),
    (16,5,4,2,NULL,'green',530,NULL,TRUE,'towards seabed'),
    (17,5,4,7,NULL,'green',530,NULL,TRUE,'towards seabed'),
    (18,5,4,3,NULL,'green',530,NULL,TRUE,'towards seabed'),
    (19,5,4,8,NULL,'green',530,NULL,TRUE,'towards seabed'),
    (20,5,4,1,NULL,'green',530,NULL,FALSE,'negligible'),
    (21,6,5,2,'bycatch','white',425,750,FALSE,'negligible'),
    (22,6,5,3,'bycatch','white',425,750,FALSE,'negligible'),
    (23,6,5,10,'target','white',425,750,FALSE,'negligible'),
    (24,6,5,6,'bycatch','white',425,750,FALSE,'negligible'),
    (25,6,5,8,'bycatch','white',425,750,FALSE,'negligible'),
    (26,6,5,11,'bycatch','white',425,750,FALSE,'negligible'),
    (27,7,5,6,'bycatch','white',425,750,TRUE,'escape'),
    (28,7,5,8,'bycatch','white',425,750,TRUE,'escape'),
    (29,7,5,11,'bycatch','white',425,750,TRUE,'escape'),
    (30,7,5,2,'bycatch','white',425,750,TRUE,'escape'),
    (31,8,6,9,'target','green',540,NULL,TRUE,'towards'),
    (32,8,6,1,'bycatch','green',540,NULL,TRUE,'away'),
    (33,8,6,2,'bycatch','green',540,NULL,FALSE,'negligible'),
    (34,8,6,3,'bycatch','green',540,NULL,TRUE,'towards'),
    (35,8,6,8,'bycatch','green',540,NULL,TRUE,'towards'),
    (36,8,6,11,'bycatch','green',540,NULL,FALSE,'negligible'),
    (37,9,6,1,'bycatch','green',540,NULL,FALSE,'negligible'),
    (38,9,6,2,'bycatch','green',540,NULL,TRUE,'towards'),
    (39,9,6,3,'bycatch','green',540,NULL,TRUE,'away'),
    (40,9,6,8,'bycatch','green',540,NULL,FALSE,'negligible'),
    (41,9,6,11,'bycatch','green',540,NULL,TRUE,'away'),
    (42,10,7,1,'target','green',523,NULL,TRUE,'towards'),
    (43,11,7,1,'target','green',523,NULL,TRUE,'towards'),
    (44,12,8,12,'target','white',425,750,FALSE,'negligible'),
    (45,13,8,12,'target','white',425,750,FALSE,'negligible'),
    (46,12,8,13,'target','white',425,750,FALSE,'negligible'),
    (47,13,8,13,'target','white',425,750,FALSE,'negligible'),
    (48,14,9,12,'target','blue',465,NULL,FALSE,'negligible'),
    (49,14,9,14,'bycatch','blue',465,NULL,FALSE,'negligible'),
    (50,14,9,13,'bycatch','blue',465,NULL,TRUE,'erratic escape'),
    (51,15,10,1,'target','green',523,NULL,FALSE,'negligible'),
    (52,15,10,1,'target','white',425,750,TRUE,'towards'),
    (53,16,10,1,'target','white',425,750,TRUE,'towards'),
    (54,16,10,15,'bycatch','white',425,750,TRUE,'towards'),
    (55,17,11,16,'target','white',456,NULL,TRUE,'towards'),
    (56,17,11,16,'target','blue',464,NULL,TRUE,'towards'),
    (57,17,11,16,'target','green',519,NULL,FALSE,'negligible'),
    (58,17,11,16,'target','red',632,NULL,FALSE,'negligible'),
    (59,17,11,16,'target','purple',446,NULL,TRUE,'away'),
    (60,18,11,16,'target','white',456,NULL,TRUE,'towards'),
    (61,18,11,16,'target','purple',446,NULL,TRUE,'towards'),
    (62,19,11,16,'target','blue',464,NULL,TRUE,'towards'),
    (63,19,11,16,'target','green',519,NULL,TRUE,'towards'),
    (64,19,11,16,'target','white',456,NULL,TRUE,'towards'),
    (65,19,11,16,'target','red',632,NULL,FALSE,'negligible'),
    (66,19,11,16,'target','purple',446,NULL,FALSE,'negligible'),
    (67,20,12,17,'bycatch','blue',464,NULL,TRUE,'escape'),
    (68,21,12,17,'bycatch','blue',464,NULL,TRUE,'escape');
```

```{attention}
I will write a data upload interface for new studies. MySQL saves databases as csv files. 
If we needed to relocate or resurrect in any way, we would load and read csv files directly, rather than write screeds of INSERT INTO lines.
```