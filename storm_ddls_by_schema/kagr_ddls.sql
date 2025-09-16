-- ============================================================
-- DDL STATEMENTS FOR SCHEMA: KAGR
-- Generated on: 2025-09-11 17:17:36
-- Objects: 44
-- ============================================================

-- Set schema context
USE SCHEMA KAGR;

-- Object: DIM_CUSTOMER
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_CUSTOMER
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

-- Object: DIM_CUSTOMER_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_CUSTOMER_HISTORY
(
   
   CUSTOMERKEY        NUMBER(38, 0);

-- Object: DIM_DATE
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_DATE
         (
          DATEKEY,
          SKHASH,
          TEAMABBREVIATION,
          DATE,
          DAYOFMONTH,
          DAYSUFFIX,
          DAYNAME,
          DAYOFWEEK,
          DAYOFWEEKINMONTH,
          DAYOFWEEKINYEAR,
          DAYOFQUARTER,
          DAYOFYEAR,
          WEEKOFMONTH,
          WEEKOFQUARTER,
          WEEKOFYEAR,
          MONTH,
          MONTHNAME,
          MONTHOFQUARTER,
          QUARTER,
          QUARTERNAME,
          QUARTERYEAR,
          YEAR,
          MONTHYEAR,
          FIRSTDAYOFMONTH,
          LASTDAYOFMONTH,
          FIRSTDAYOFQUARTER,
          LASTDAYOFQUARTER,
          FIRSTDAYOFYEAR,
          LASTDAYOFYEAR,
          ISHOLIDAY,
          ISWEEKDAY,
          HOLIDAYNAME,
          ACTIVE, 
          DWINSERTDATE,
          DWUPDATEDATE
            );

-- Object: DIM_DATE_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_DATE_HISTORY
(
   
   DATEKEY           NUMBER(38, 0);

-- Object: DIM_EVENT
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_EVENT(
	EVENTKEY ,
	SKHASH ,
	TEAMABBREVIATION  ,
	SEASONKEY ,
	EVENTCODE ,
	EVENTNAME ,
	EVENTDATE ,
	EVENTTIME ,
	EVENTANDDATE ,
	SEASONGROUPINGNAME ,
	EVENTTYPE ,
	EVENTSUBTYPE ,
	EVENTTIER ,
	OPPONENT ,
	OPPONENTDIVISION ,
	OPPONENTCONFERENCE ,
	VOIDEDEVENTFLAG ,
	VENUE ,
	LEAGUE ,
	ACTIVE 
);

-- Object: DIM_EVENT_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_EVENT_HISTORY (
	EVENTKEY NUMBER(38,0);

-- Object: DIM_MANIFEST
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_MANIFEST
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

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_MANIFEST
         (
   MANIFESTKEY      , 
   SKHASH           ,
   TEAMABBREVIATION ,
   SEASONYEAR       ,
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
   ACTIVE           
);

-- Object: DIM_MANIFEST_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_MANIFEST_HISTORY
(
   MANIFESTKEY      VARCHAR();

-- Object: DIM_MANIFEST_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_MANIFEST_HISTORY
(
   TEAMABBREVIATION VARCHAR();

-- Object: DIM_PAYMENTMETHOD
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_PAYMENTMETHOD
         (
          PAYMENTMETHODKEY,
          TEAMABBREVIATION,
          SKHASH,
          PAYMETHODCODE,
          PAYMETHODNAME,
          ACTIVE,
          DWINSERTDATE,
          DWUPDATEDATE
         );

-- Object: DIM_PAYMENTMETHOD
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_PAYMENTMETHOD
    (
    PAYMENTMETHODKEY,
    TEAMABBREVIATION,
    SKHASH,
    PAYMETHODCODE,
    PAYMETHODNAME,
    ACTIVE,
    DWINSERTDATE,
    DWUPDATEDATE
    );

-- Object: DIM_PAYMENTMETHOD_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PAYMENTMETHOD_HISTORY
(
    PAYMENTMETHODKEY NUMBER(38, 0);

-- Object: DIM_PAYMENTMETHOD_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PAYMENTMETHOD_HISTORY
(
   PAYMENTMETHODKEY NUMBER(38, 0);

-- Object: DIM_PLANGROUPING
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_PLANGROUPING
         (
          PLANGROUPINGKEY,
          SKHASH,
          TEAMABBREVIATION,
          SOURCE,
          PLANCODE,
          PLANNAME,
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

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_PLANGROUPING(
   PLANGROUPINGKEY   ,
   SKHASH            ,
   TEAMABBREVIATION  ,
   PLANCODE          ,
   PLANNAME          ,
   PLANTYPE          ,
   PLANSUBTYPE       ,
   PRORATEDINDICATOR ,
   FSEMULTIPLIER     ,
   EVENTSINPLAN      ,
   ACTIVE            
);

-- Object: DIM_PLANGROUPING
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_PLANGROUPING(
   PLANGROUPINGKEY   ,
   SKHASH            ,
   TEAMABBREVIATION  ,
   PLANCODE          ,
   PLANNAME          ,
   PLANTYPE          ,
   PLANSUBTYPE       ,
   PRORATEDINDICATOR ,
   FSEMULTIPLIER     ,
   EVENTSINPLAN      ,
   ACTIVE            
);

-- Object: DIM_PLANGROUPING_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PLANGROUPING_HISTORY
(
   PLANGROUPINGKEY   NUMBER(38, 0);

-- Object: DIM_PLANGROUPING_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PLANGROUPING_HISTORY
(
   PLANGROUPINGKEY   NUMBER(38, 0);

-- Object: DIM_PLANGROUPING_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PLANGROUPING_HISTORY
(
   PLANGROUPINGKEY   NUMBER(38, 0);

-- Object: DIM_PRICECODE
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_PRICECODE(
      PRICECODEKEY         ,
      SKHASH               ,
      TEAMABBREVIATION     ,
      PRICECODE            ,
      PRICECODEGROUP       ,
      PRICECODEDESCRIPTION ,
      ACTIVE               ,
      DWINSERTDATE         ,
      DWUPDATEDATE         
        );

-- Object: DIM_PRICECODE_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PRICECODE_HISTORY
(
   PRICECODEKEY         NUMBER(38, 0);

-- Object: DIM_PRICECODE_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PRICECODE_HISTORY
(
   PRICECODEKEY         NUMBER(38, 0);

-- Object: DIM_PROMOTION
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_PROMOTION
(       
   PROMOTIONKEY      ,
   SKHASH            ,
   TEAMABBREVIATION  ,
   SOURCE            ,
   PROMOTIONCODE     ,
   PROMOTIONNAME     ,
   PROMOTIONGROUPING ,
   ACTIVE                
         
         );

-- Object: DIM_PROMOTION_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_PROMOTION_HISTORY
(
   PROMOTIONKEY      NUMBER(38, 0);

-- Object: DIM_SEASON
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_SEASON
(
	SEASONKEY,
	SKHASH,
	TEAMABBREVIATION,
	SOURCE,
	ACTIVEFROMDATE,
	ACTIVETODATE,
	ACTIVEINDICATOR,
	SEASONYEAR,
	SEASONNAME,
	TEAM,
	ACTIVE
);

-- Object: DIM_SEASONYEAR
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_SEASONYEAR
         (
   SEASONYEARKEY      ,
   TEAMABBREVIATION   ,
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

CREATE TABLE IF NOT EXISTS KAGR.DIM_SEASONYEAR_HISTORY
(
   SEASONYEARKEY      NUMBER(38,0);

-- Object: DIM_SEASON_HISTORY
-- --------------------------------------------------

CREATE OR REPLACE TABLE KAGR.DIM_SEASON_HISTORY (
	SEASONKEY NUMBER(38,0);

-- Object: DIM_SEATMAP
-- --------------------------------------------------

create or replace materialized view KAGR.DIM_SEATMAP(
	SEASONMAPKEY,
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

create or replace TABLE KAGR.DIM_SEATMAP_HISTORY (
	SEASONMAPKEY NUMBER(38,0);

-- Object: DIM_STADIUMENTRY
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_STADIUMENTRY
         (
   STADIUMENTRYKEY    ,
   SKHASH             ,
   TEAMABBREVIATION   ,
   GATECODE           ,
   GATENAME           ,
   GATEGROUPING       ,
   ACTIVE             
            );

-- Object: DIM_STADIUMENTRY
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.DIM_STADIUMENTRY
(
    STADIUMENTRYKEY    ,
    SKHASH             ,
    TEAMABBREVIATION   ,
    GATECODE           ,
    GATENAME           ,
    GATEGROUPING       ,
    ACTIVE             
);

-- Object: DIM_STADIUMENTRY_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_STADIUMENTRY_HISTORY
(
    STADIUMENTRYKEY   NUMBER(38, 0);

-- Object: DIM_STADIUMENTRY_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.DIM_STADIUMENTRY_HISTORY
(
   STADIUMENTRYKEY   NUMBER(38, 0);

-- Object: DIM_STADIUMMAP_HISTORY
-- --------------------------------------------------

create or replace TABLE KAGR.DIM_STADIUMMAP_HISTORY (
	STADIUMAPKEY NUMBER(38,0);

-- Object: DIM_STM_HISTORY
-- --------------------------------------------------

CREATE OR REPLACE TABLE KAGR.DIM_STM_HISTORY (
	SKHASH VARCHAR();

-- Object: FACT_MARKETPLACE
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.FACT_MARKETPLACE
(
   MARKETPLACEKEY,
   TEAMABBREVIATION,
   RAWSOURCE,
   RECORDSOURCE,
   MARKETPLACE,
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
   ORDERNUMBER,
   TRANSACTIONID,
   ORIGINALPOSTINGDATE,
   ORIGINALPOSTINGPRICE,
   ACTIVE
);

-- Object: FACT_MARKETPLACE_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.FACT_MARKETPLACE_HISTORY (
      TEAMABBREVIATION VARCHAR(16777216);

-- Object: FACT_PLAN
-- --------------------------------------------------

CREATE OR REPLACE MATERIALIZED VIEW KAGR.FACT_PLAN(
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

CREATE OR REPLACE TABLE KAGR.FACT_PLAN_HISTORY (
	PLANKEY NUMBER(38,0);

-- Object: FACT_SEAT_HISTORY
-- --------------------------------------------------

CREATE OR REPLACE TABLE KAGR.FACT_SEAT_HISTORY (
	TEAMABBREVIATION VARCHAR();

-- Object: FACT_TICKETINGORDER
-- --------------------------------------------------

CREATE
OR REPLACE MATERIALIZED VIEW KAGR.FACT_TICKETINGORDER (
    TICKETINGORDERKEY,
    SKHASH,
    RAWSOURCE,
    TEAMABBREVIATION,
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
    ORDERNUMBER,
    ACTIVE,
    DWINSERTDATE,
    DWUPDATEDATE
);

-- Object: FACT_TICKETINGORDER_HISTORY
-- --------------------------------------------------

CREATE TABLE IF NOT EXISTS KAGR.FACT_TICKETINGORDER_HISTORY
(
TICKETINGORDERKEY     NUMBER(38, 0);

-- End of KAGR DDL statements
