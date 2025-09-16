-- ============================================================
-- DDL STATEMENTS FOR SCHEMA: STAGE
-- Generated on: 2025-09-11 17:17:36
-- Objects: 61
-- ============================================================

-- Set schema context
USE SCHEMA STAGE;

-- Object: ARCHTICSINVENTORY_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSINVENTORY_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: ARCHTICSINVENTORY_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSINVENTORY_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: ARCHTICSTICKETEXCHANGE_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSTICKETEXCHANGE_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: ARCHTICSTICKETEXCHANGE_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSTICKETEXCHANGE_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: ARCHTICSTICKETEXCHANGE_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSTICKETEXCHANGE_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(6);

-- Object: ARCHTICSTICKETEXCHANGE_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSTICKETEXCHANGE_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(6);

-- Object: ARCHTICSTICKETEXPANDED_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSTICKETEXPANDED_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: ARCHTICSTICKETEXPANDED_SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.ARCHTICSTICKETEXPANDED_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: DIM_CUSTOMER
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_CUSTOMER
         (
                CUSTOMERKEY        ,
                TEAMABBREVIATION   ,
                SOURCE             ,
                RAWAUDIENCEID      , 
                BUSINESSINDICATOR  ,
                ACQUISITIONTENURE  ,
                EMAILCONTACTABLE   ,
                PHONECONTACTABLE   ,
                ADDRESSCONTACTABLE ,
                ADDRESS1           ,
                ADDRESS2           ,
                CITY               ,
                ZIP                ,
                STATE              ,
                COUNTY             ,
                COUNTRY            ,
                DISTANCETOVENUE    ,
                EMAILADDRESS       ,
                PHONENUMBER        ,
                GENDER             ,
                CUSTOMERTYPE       ,
                AUDIENCEID         ,
                FIRSTNAME          ,
                LASTNAME           ,
                FULLNAME           ,
                ACCOUNTTYPE        ,
                DISPLAYACCOUNTID   ,
                CUSTOMERSINCE      ,
                ACTIVE             
            );

-- Object: DIM_CUSTOMER
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_CUSTOMER
         (
          RAWAUDIENCEID,
          TEAMABBREVIATION,
          BUSINESSINDICATOR,
          ACQUISITIONTENURE,
          EMAILCONTACTABLE,
          PHONECONTACTABLE,
          ADDRESSCONTACTABLE,
          ADDRESS1,
          ADDRESS2,
          CITY,
          ZIP,
          STATE,
          COUNTY,
          COUNTRY,
          DISTANCETOVENUE,
          EMAILADDRESS,
          PHONENUMBER,
          GENDER,
          CUSTOMERTYPE,
          AUDIENCEID,
          FIRSTNAME,
          LASTNAME,
          FULLNAME,
          ACCOUNTTYPE,
          SOURCE,
          DISPLAYACCOUNTID,
          CUSTOMERSINCE,
          ACTIVE,
          DWINSERTDATE,
          DWUPDATEDATE
         );

-- Object: DIM_CUSTOMERPYRAMID
-- --------------------------------------------------

CREATE
OR REPLACE MATERIALIZED VIEW STAGE.DIM_CUSTOMERPYRAMID (
	AUDIENCEID,
	SOURCENUMBER,
	SOURCENAME,
	LEVEL1,
	STARTDATE,
	MOSTRECENTRUNDATETIME,
	ACTIVE,
	DWINSERTDATE,
	DWUPDATEDATE
);

-- Object: DIM_CUSTOMERPYRAMID_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_CUSTOMERPYRAMID_HISTORY (
	AUDIENCEID NUMBER (38, 0);

-- Object: DIM_CUSTOMER_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_CUSTOMER_HISTORY
(
   
   CUSTOMERKEY        NUMBER(38, 0);

-- Object: DIM_DATE_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_DATE_HISTORY
(
   DATEKEY           NUMBER(38, 0);

-- Object: DIM_EVENT
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_EVENT(
	EVENTKEY ,
	SKHASH ,
	TEAMABBREVIATION  ,
	SOURCE ,
	SEASONKEY ,
	EVENTCODE ,
	EVENTNAME ,
	EVENTNAMECLEAN ,
	EVENTDATE ,
	EVENTTIME ,
	EVENTANDDATE ,
	SEASONGROUPINGNAME ,
	SEASONTYPE ,
	EVENTTYPE ,
	EVENTSUBTYPE ,
	EVENTTIER ,
	OPPONENT ,
	OPPONENTDIVISION ,
	OPPONENTCONFERENCE ,
	VOIDEDEVENTFLAG ,
	WEEK ,
	DAYANDTIME ,
	QUALITYOFOPPONENT ,
	TIER,
	SPECIALEVENT ,
	VENUE ,
	MAJORCATEGORY ,
	MINORCATEGORY ,
	LEAGUE ,
	ACTIVE 
	
);

-- Object: DIM_EVENT_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_EVENT_HISTORY (
	EVENTKEY NUMBER(38,0);

-- Object: DIM_MANIFEST
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_MANIFEST
         (
          TEAMABBREVIATION,
          SKHASH,
          SEASONYEAR,
          MANIFESTID,
          SEASONID,
          SECTIONNAME,
          ROWNAME,
          SEATS,
          CAPACITY,
          CLASSNAME,
          CLASSIFICATION,
          STADIUMLEVEL,
          ROWLEVEL,
          ROWSORTORDER,
          STADIUMSIDE,
          SIGHTLINE,
          BASECATEGORY,
          DESCRIPTION,
          ORGANIZATIONNAME,
          ACTIVE,
          DWINSERTDATE,
          DWUPDATEDATE
         );

-- Object: DIM_MANIFEST
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_MANIFEST
         (
   MANIFESTKEY      , 
   SKHASH           ,
   TEAMABBREVIATION ,
   SEASONYEAR       ,
   MANIFESTID       ,
   SEASONID         ,
   SECTIONNAME      ,
   ROWNAME          ,
   SEATS            ,
   CAPACITY         ,
   CLASSNAME        ,
   CLASSIFICATION   ,
   STADIUMLEVEL     ,
   ROWLEVEL         ,
   ROWSORTORDER     ,
   STADIUMSIDE      ,
   SIGHTLINE        ,
   BASECATEGORY     ,
   DESCRIPTION      ,
   ORGANIZATIONNAME ,
   ACTIVE             
            );

-- Object: DIM_MANIFEST_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_MANIFEST_HISTORY
(
   MANIFESTKEY      VARCHAR();

-- Object: DIM_MANIFEST_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_MANIFEST_HISTORY
(
   TEAMABBREVIATION VARCHAR();

-- Object: DIM_PAYMENTMETHOD
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PAYMENTMETHOD
(
          PAYMENTMETHODKEY,
          SKHASH,
          TEAMABBREVIATION,
          SOURCE,
          PAYMETHODCODE,
          PAYMETHODNAME,
          ACTIVE
);

-- Object: DIM_PAYMENTMETHOD
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PAYMENTMETHOD
(
    PAYMENTMETHODKEY,
    SKHASH,
    TEAMABBREVIATION,
    SOURCE,
    PAYMETHODCODE,
    PAYMETHODNAME,
    ACTIVE
);

-- Object: DIM_PAYMENTMETHOD_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PAYMENTMETHOD_HISTORY
(
    PAYMENTMETHODKEY NUMBER(38, 0);

-- Object: DIM_PAYMENTMETHOD_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PAYMENTMETHOD_HISTORY
(
   PAYMENTMETHODKEY NUMBER(38, 0);

-- Object: DIM_PLANGROUPING
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PLANGROUPING
         (
          PLANGROUPINGKEY,
          SKHASH,
          TEAMABBREVIATION,
          SOURCE,
          PLANCODE,
          PLANNAME,
          PRICECODE,
          PLANTYPE,
          PLANSUBTYPE,
          PRORATEDINDICATOR,
          FSEMULTIPLIER,
          EVENTSINPLAN,
          SEASONID,
          ACTIVE,
          DWINSERTDATE,
          DWUPDATEDATE
         );

-- Object: DIM_PLANGROUPING
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PLANGROUPING(
   PLANGROUPINGKEY   ,
   SKHASH            ,
   TEAMABBREVIATION  ,
   SOURCE            ,
   PLANCODE          ,
   PLANNAME          ,
   PRICECODE         ,
   PLANTYPE          ,
   PLANSUBTYPE       ,
   PRORATEDINDICATOR ,
   FSEMULTIPLIER     ,
   EVENTSINPLAN      ,
   SEASONID          ,
   ACTIVE            
);

-- Object: DIM_PLANGROUPING
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PLANGROUPING(
   PLANGROUPINGKEY   ,
   SKHASH            ,
   TEAMABBREVIATION  ,
   SOURCE            ,
   PLANCODE          ,
   PLANNAME          ,
   PRICECODE         ,
   PLANTYPE          ,
   PLANSUBTYPE       ,
   PRORATEDINDICATOR ,
   FSEMULTIPLIER     ,
   EVENTSINPLAN      ,
   SEASONID          ,
   ACTIVE            
);

-- Object: DIM_PLANGROUPING_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PLANGROUPING_HISTORY
(
   PLANGROUPINGKEY   NUMBER(38, 0);

-- Object: DIM_PLANGROUPING_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PLANGROUPING_HISTORY
(
   PLANGROUPINGKEY   NUMBER(38, 0);

-- Object: DIM_PLANGROUPING_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PLANGROUPING_HISTORY
(
   PLANGROUPINGKEY   NUMBER(38, 0);

-- Object: DIM_PRICECODE
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PRICECODE
         (
      PRICECODEKEY         ,
      SKHASH               ,
      TEAMABBREVIATION     ,
      SOURCE               ,
      SEASONID             ,
      PRICECODE            ,
      PRICECODEGROUP       ,
      PRICECODEDESCRIPTION ,
      ACTIVE               , 
      DWINSERTDATE         ,
      DWUPDATEDATE         
            );

-- Object: DIM_PRICECODE
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PRICECODE
         (PRICECODEKEY,
          TEAMABBREVIATION,
          SOURCE,
          SKHASH,
          SEASONID,
          PRICECODE,
          PRICECODEDESCRIPTION,
          PRICECODEGROUP,
          ACTIVE,
          DWINSERTDATE,
          DWUPDATEDATE
         );

-- Object: DIM_PRICECODE_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PRICECODE_HISTORY
(
   PRICECODEKEY NUMBER(38, 0);

-- Object: DIM_PRICECODE_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.DIM_PRICECODE_HISTORY (
   PRICECODEKEY         NUMBER(38, 0);

-- Object: DIM_PROMOTION
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PROMOTION
         (
          PROMOTIONKEY      ,
          SKHASH            ,
          TEAMABBREVIATION  ,
          SOURCE            ,
          SEASONID          ,
          EVENTID           ,
          PROMOTIONCODE     ,
          PROMOTIONNAME     ,
          PROMOTIONGROUPING ,
          ACTIVE            
            );

-- Object: DIM_PROMOTION
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_PROMOTION
         (
          TEAMABBREVIATION,
          SOURCE,
          SKHASH,
          SEASONID,
          EVENTID,
          PROMOTIONCODE,
          PROMOTIONNAME,
          PROMOTIONGROUPING,
          ACTIVE,
          DWINSERTDATE,
          DWUPDATEDATE
         );

-- Object: DIM_PROMOTION_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PROMOTION_HISTORY
(
   PROMOTIONKEY      NUMBER(38, 0);

-- Object: DIM_PROMOTION_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_PROMOTION_HISTORY
(
   TEAMABBREVIATION  VARCHAR();

-- Object: DIM_SEASON
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_SEASON(
	SEASONKEY,
	SEASONID,
	ARENAID,
	SKHASH,
	DWINSERTDATE,
	DWUPDATEDATE,
	ACTIVEFROMDATE,
	ACTIVETODATE,
	ACTIVEINDICATOR,
	SEASONYEAR,
	SEASONNAME,
	MANIFESTID,
	TEAM,
	TEAMABBREVIATION,
	SOURCE,
	ACTIVE
);

-- Object: DIM_SEASONYEAR
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_SEASONYEAR
(
   SEASONYEARKEY      ,
   TEAMABBREVIATION   ,
   NAME               ,
   SKHASH             ,
   PREVIOUSSEASONKEY  ,
   CURRENTSEASONKEY   ,
   PREVIOUSSEASONYEAR  ,
   CURRENTSEASONYEAR   ,
   NEXTSEASONYEAR     ,
   SEASONNAME         ,
   LOGICDESCRIPTION   ,
   ACTIVEFROMDATE     ,
   ACTIVETODATE       ,
   ACTIVE             
);

-- Object: DIM_SEASONYEAR_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_SEASONYEAR_HISTORY
(
   SEASONYEARKEY      NUMBER(38,0);

-- Object: DIM_SEASON_HISTORY
-- --------------------------------------------------

CREATE OR REPLACE TABLE STAGE.DIM_SEASON_HISTORY (
    SEASONKEY NUMBER (38, 0);

-- Object: DIM_SEATMAP
-- --------------------------------------------------

create or replace materialized view STAGE.DIM_SEATMAP(
	SEASONKEY,
	TEAMABBREVIATION,
	ROWNAME,
	SEAT,
	SECTION,
	X,
	Y,
	SECTIONMAPPING,
	DWINSERTDATE,
	DWUPDATEDATE,
	ACTIVE
);

-- Object: DIM_SEATMAP_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.DIM_SEATMAP_HISTORY (
    SEASONMAPKEY NUMBER(38,0);

-- Object: DIM_STADIUMENTRY
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_STADIUMENTRY
         (
   STADIUMENTRYKEY    ,
   SKHASH             ,
   TEAMABBREVIATION   ,
   SOURCE             ,
   SEASONID           ,
   GATECODE           ,
   GATENAME           ,
   GATEGROUPING       ,
   ACTIVE             
            );

-- Object: DIM_STADIUMENTRY
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.DIM_STADIUMENTRY
(
    STADIUMENTRYKEY    ,
    SKHASH             ,
    TEAMABBREVIATION   ,
    SOURCE             ,
    SEASONID           ,
    GATECODE           ,
    GATENAME           ,
    GATEGROUPING       ,
    ACTIVE             
);

-- Object: DIM_STADIUMENTRY_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_STADIUMENTRY_HISTORY
(

    STADIUMENTRYKEY NUMBER(38, 0);

-- Object: DIM_STADIUMENTRY_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.DIM_STADIUMENTRY_HISTORY
(
   
   STADIUMENTRYKEY NUMBER(38, 0);

-- Object: DIM_STADIUMMAP
-- --------------------------------------------------

create or replace materialized view STAGE.DIM_STADIUMMAP(
	STADIUMAPKEY,
	SKHASH,
	DWINSERTDATE,
	DWUPDATEDATE,
	TEAMABBREVIATION,
	SEASONKEY,
	SECTION,
	POLYGON,
	POINTORDER,
	X,
	Y,
	RECORDINDICATOR,
	ACTIVE
);

-- Object: DIM_STADIUMMAP_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.DIM_STADIUMMAP_HISTORY (
	STADIUMAPKEY NUMBER(38,0);

-- Object: DIM_STM_HISTORY
-- --------------------------------------------------

CREATE OR REPLACE TABLE STAGE.DIM_STM_HISTORY (
	SKHASH VARCHAR();

-- Object: FACT_MARKETPLACE
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.FACT_MARKETPLACE
         (
          TEAMABBREVIATION,
          RECORDSOURCE,
          MARKETPLACE,
          ORDERNUMBER,
          ORDERLINEITEM,
          EVENTID,
          ORDERLINEITEMSEQUENCE,
          SEQUENCENUMBER,
          SEQUENCEID,
          TRANSACTIONID,
          LISTINGID,
          RAWSOURCE,
          BLOCKHASH,
          SKHASH,
          DWINSERTDATE,
          DWUPDATEDATE,
          BUYERCUSTOMERKEY,
          SELLERCUSTOMERKEY,
          ACTIVITYDATEKEY,
          PAYMENTMETHODKEY,
          SEASONKEY,
          EVENTKEY,
          PRICECODEKEY,
          PROMOTIONKEY,
          ACTIVITYDATE,
          ACTIVITYTYPE,
          QUANTITY,
          REVENUE,
          POSTINGPRICE,
          BUYERFEES,
          SELLERFEES,
          DELIVERYFEES,
          TAXES,
          SEATBLOCKS,
          RECORDINDICATORASC,
          RECORDINDICATORDESC,
          LISTINGSTATUS,
          ACTIVITYNAME,
          LISTINGHASH,
          LISTINGSEGMENTHASH,
          ORIGINALPOSTINGPRICE,
          ORIGINALPOSTINGDATE,
          TEMPRECORDIND,
          ACTIVE
            );

-- Object: FACT_MARKETPLACE_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.FACT_MARKETPLACE_HISTORY (
      TEAMABBREVIATION VARCHAR(16777216);

-- Object: FACT_PLAN
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.FACT_PLAN(
	PLANKEY,
	TEAMABBREVIATION,
	SKHASH,
	REVENUEINPLANPERSEAT,
	SEASONID,
	SEASONKEY,
	FULLPAYMENTDATE,
	RENEWALKEY,
	CANCELINDICATOR,
	COMPINDICATOR,
	CUSTOMERKEY,
	FIRSTPAYMENTDATE,
	LASTPAYMENTDATE,
	ORDERLINEITEM,
	ORDERNUMBER,
	PLANEVENTID,
	PLANEVENTNAME,
	PLANGROUPINGKEY,
	--PAYMENTPLANKEY,
	PRICECODE,
	PSLINDICATOR,
	RAWAUDIENCEID,
	RENEWALSTATUS,
	DWINSERTDATE,
	DWUPDATEDATE,
	ACTIVE
);

-- Object: FACT_PLAN_HISTORY
-- --------------------------------------------------

CREATE OR REPLACE TABLE STAGE.FACT_PLAN_HISTORY (
	PLANKEY NUMBER(38,0);

-- Object: FACT_SEAT_HISTORY
-- --------------------------------------------------

CREATE OR REPLACE TABLE STAGE.FACT_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR();

-- Object: FACT_TICKETINGORDER
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW STAGE.FACT_TICKETINGORDER (
    TICKETINGORDERKEY,
    SKHASH,
    TEAMABBREVIATION,
    RAWSOURCE,
    ORDERNUMBER,
    ORDERLINEITEM,
    ORDERLINEITEMSEQUENCE,
    SEQUENCENUMBER,
    TICKETSEQUENCEID,
    EVENTID,
    SECTIONNAME,
    ROWNAME,
    FIRSTSEAT,
    LASTSEAT,
    BILLINGCUSTOMERKEY,
    SHIPPINGCUSTOMERKEY,
    PAYMENTPLANKEY,
    PAYMENTMETHODKEY,
    SEASONKEY,
    ORDERDATEKEY,
    PRICECODEKEY,
    EVENTKEY,
    PROMOTIONKEY,
    REVENUEPERSEAT,
    ORIGINALPURCHASEPRICE,
    CURRENTPURCHASEPRICE,
    CURRENTREVENUE,
    SELLERFEE,
    BUYERFEE,
    DELIVERYFEE,
    TAXES,
    NUMBEROFSEATS,
    ORDERDATE,
    LASTPAYMENTDATE,
    ORDERSTATUS,
    POSTINGPRICE,
    SOURCE,
    ACTIVE,
    DWINSERTDATE,
    DWUPDATEDATE
);

-- Object: FACT_TICKETINGORDER_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.FACT_TICKETINGORDER_HISTORY
(
TICKETINGORDERKEY     NUMBER(38, 0);

-- Object: SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: SEAT_HISTORY
-- --------------------------------------------------

create or replace TABLE STAGE.SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR(16777216);

-- Object: STMSEATS_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS STAGE.STMSEATS_HISTORY (
    TEAMABBREVIATION VARCHAR DEFAULT '&teamAbbr',
    SKHASH VARCHAR(16777216);

-- End of STAGE DDL statements
