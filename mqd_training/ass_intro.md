# Background #

The market above should be added to the WorkFlow/MQD in the time
range 1Jan 2017-1July2017.

- Note upfront. If you see any market settings in market config,
  take them with caution and assume these are false. We changed
  our complete approach, and hence every aspect of setting up a
  market should be checked/verified.

- *All documents need to be collected in this Jira and all
  alterations should be done using this Jira.*

# Expectations #

1/4 page summary about the main exchange, its markets and what is
traded, whether there are different market segments etc.

In cmcrc-marketconfig-data, we collect all information about the
markets. The relevant settings were discussed in session 2/3, the
following points 1)-12) might not be complete, but give a
guidance.

## 1. Types & Regex: ##

a. Download the official instrument list from the homepage of
the exchange of all traded equities and etf. The date of effect
of this list decides about the test period you will need to run
on our WorkFlow system This might not be within the above
mentioned time period, but more recent. At the same time please
look for any documentation about volume, number of trades or
similar on security (and market) level. It is recommended to 

  1. have the instrument list in both, ISIN and Ric format, and 

  2. note the date of effect

Load the list in TRTH to get an idea what types we need to
download to cover all securities needed, usually 112/113 but it
could be 97/96.

Adapt types in streams file in PyCharm. Even if currently there
are no funds, please always add type 112 as there might have been
funds in earlier times.

Request these types in TRTH for the period you have official data
for to compare. This can be just a day or a week/ month dependent
how the official source reports data. Build a Ric-Isin list from
the TRTH data.

Please compare the 2 lists, the TRTH list and the list from the
exchange, in both directions via vlookup in excel. The aim is
to replicate the list from the exchange with the TRTH data.
Often we need to exclude securities. Identify patterns of the
rics in the official list and rules to separate them from not
necessary, but reported rics in TRTH -> Regex. (See also
Session2/5). We prefer regex over fix exclusions, since these
are more flexible.

The instrument list is crucial. Once you think you have found
the relevant regex/settings, please verify with your mentor.

b. Run the test period till daily stats in the WorkFlow.
Compare the sync data (again) with the official list: Should we
filter out some? Note, we aim to cover instruments of equity
and funds as named on the instrument lists. Often TRTH presents
other rics within 112/113 which we are not interested in as
warrants or fixed income bonds. Do vlookup in both directions,
the MQD file and the official list.

If the final list is not matching or mismatches cannot be
explained (no trading or else) then we need to write additional
filter to filter those out in the convert step as that saves
space and processing time. We call them regex filter, see GER
or LSE yaml for that. Adapt the filter till the lists match.
Adapt the feeds yaml file in PyCharm further (See also session
5)

## 2. Qualifier ##

Trades are classified through qualifiers indicated the kind of
trade. We need to read those to process data in the correct way.

Link to the qualifier list was given in session 4.

Try to get an understanding what each qualifier means, you can
add comments in the yaml file so a third person can easily
follow

## 3. Trading hours ##

Find trading hours, add them to yaml files.

open: opening time

close: closing time, see LSE as example.

Regarding the closing time, TRTH is sometimes displaying trades
delayed. The market might close officially at 18:30 but the last
trade in TRTH might be displayed at 18:30:27. We need to adapt
the closing time to the actual TRTH closing time, otherwise we
would miss the last trades. Please request the closing session of
a liquid security in TRTH and try to find the last onmarket trade
and decide whether the closing time needs to be adapted.

## 4. Check the raw data ##

Request one day trading and quotes of a liquid security and have
a look whether there are any strange things, as trades without
volume or price, qualifiers we do not have etc.? If so, ask a
senior person to have a look (see also session 5)

## 5 trading and listing market. yaml ##

Please have a look in these files in Pycharm. Is the market
there? If you compare it to main markets as LSE or US markets do
you have the feeling something is missing?

## 6. tracks.yaml ##

Please have a look in this file which defines which convert jobs
will be available.The market should be specified there five
times.

## 7. Public Holidays ##

please adapt the public holidays file in pycharm: collect public
holidays (bank holidays) of at least the past 3 years till 1/1/18
and add them in the public holiday file in pycharm in the style:

20171225 Christmas Day. 

Half trading days need to be handled in the trading hours section
in the streams file, please see lse.

Please document everything and save all files in this ticket. Ask
any member of the business team if you need help.

Changes in Pycharm need to be commited and pushed in a new branch
each time, please do that in this ticket.

## 8. Initial QA - comparison with official stats - See session 5 ##

If you are finished, you will need to download test data on the
WorkFlow, let the WorkFlow run incl. daily stats. When finished
you can verify the results on MQD-QA, by downloading the daily
stats data and qa it with the official data of the exchange. The
time horizon you will need to qa depends on the data
availability, see point 1. QA needs to be done on a security base
and market level.

You have 1.5 weeks to adapt the yaml file max. Please let your
mentor know when you think you are finished.

Once you have you are sure that your market settings are correct
and the out put data matches the official data as far as you can
tell

## 9. Download the data ##

which is needed to run the following metrics from 1Jan2017-1July2017:
Daily stats
Quoted Spread
Effective Spread
Variance ratio
Daily adjusted return

## 10. Create relevant dependencies for your market ##

## 11. Run the jobs, eventually fix errors ##

Once the sync jobs are completed and successful the data is on
the MQD (QA)

## 12. QA the metrics on a market level ##

You will need to QA the results when the WorkFlow is completed.
Address irregularities as spikes, drops and structure breaks. Add
warnings where needed. You might need to adapt the market config
file. (Session 5/6)

In addition to applying your knowledge about the requirements to
set up a market correctly, please apply what you have learned
within the Uptick course and session 7 here:

## 13. Create a new metric on Jupyter ##

Create a rolling 5-days-adjusted-return metric and plot
