

[Music]

**Greg:**  
All right, hello everyone, welcome to cost optimizing existing Amazon DynamoDB workloads. My name is Greg Krohn, I'm a senior DynamoDB specialist solution architect with AWS.

**Greg:**  
I'm joined today by Julie Patil, a solutions architect for DynamoDB as well. So let's go and get started.

**Greg:**  
So what we're here today to talk about is existing DynamoDB workload cost optimization. There's a lot of documentation out there and other talks about, you know, designing for cost from the start for your schema. But really, let's say today you've already got a DynamoDB table in production and it's costing you a little more than you expected or maybe costs aren't scaling the way you expected either. So what we want to do is we want to kind of look for some quick wins here—some optimizations we can do on the table that don't require a full redesign of your code base and really just take the best advantage of DynamoDB.

**Greg:**  
So we want to focus here on efficiently operating our table, scaling appropriately, choosing the right functionalities that DynamoDB offers and taking advantage of it. And remember, this is an iterative process—we don't just create a DynamoDB table and expect it to live on forever. Just like every other service, either on-prem or in the cloud, you always got to keep an eye on its pulse and see where things are going and optimize from there.

**Greg:**  
So what we're going to take a look at today are various approaches. We're going to start off with talking about tagging your tables. Autonomously, we really want to be able to know where our costs are coming from at the table level. We also want to figure out what capacity mode works best for our table. So we're going to discuss how to pick the right capacity mode in DynamoDB.

**Greg:**  
We also want to make sure we're right sizing our capacity. We don't want to over provision—we also don't want to under provision. There's a fine line we have to tow here, and a part of that will also choose the right auto scaling settings if we're using provisioned capacity.

**Greg:**  
From there, Julie will take over to talk about using the right table class. We've got some new launches recently that let you choose what storage class as well as some other options to fit your workload the best.

**Greg:**  
We also want to figure out if we have any unused tables or indexes. It doesn't do us any good having something provisioned but unused, and we want to know how we can find those resources and clear them out if they're not really needed.

**Greg:**  
You want to look for poor table usage patterns. There are ultimately various DynamoDB APIs that are available and not all of them work best for every option. So we're going to deep dive into what patterns maybe aren't the best long term and how to replace them.

**Greg:**  
And then we'll also talk about using event stream filtering on Lambda so extra stream events that come into your Lambda functions—maybe you don't need to process all of them, and we can filter them at the stream level.

**Greg:**  
So starting with tagging—really, in Cost Explorer everything will get lumped together if you don't tag. So when you create a DynamoDB table you want to place business tags on your table. So effectively, we need to know what table belongs to—maybe what part of your organization, what specific service, what application.

**Greg:**  
Having that tagging will let us take this graph of sort of lump billing metrics that we see in Cost Explorer. As you can see here, we're grouping by usage type. For November we saw a large spike, or at least a large amount of write capacity unit hours billed to our account, and we don't really know where to go from here in terms of who, what table, or what service is contributing—we can only see at the region level.

**Greg:**  
So now once we've put tagging in place what we can actually do is we can group by these tags in Cost Explorer. So on the left you see November had a large amount of billing contributed to a table called "tweets" in this account. Well, that lines up pretty well to that previous chart we saw for a large number of write capacity units—maybe a new service launch that loads tweets into a table—and it was kind of a one-time thing. You see December and January that that table’s billing fell off, but we really didn't know who contributed to that until we tagged these. Now we can also go further and on the right chart you see we've filtered down by the "tweets" table and now we can still group by usage type so we can break down that specific table’s billing by what kind of usage they contributed.

**Greg:**  
So we see here still that they contributed a lot of write capacity hours, which means that there are a lot of writes against that table. So let's say we have these tables in production—how do we go and tag them effectively?

**Greg:**  
Now we can go into the DynamoDB console and just use the Tag Editor that's built in. So you see on the top left we've just done a tag name or a tag key of "table name" and a tag value of "tweets". That's one way to do it. You can actually do this via the CLI—you see we have "dynamodb tag-resource" and we've added in our specific tag key and value there.

**Greg:**  
We've also made a little tagger utility that, if you follow the link at the bottom of the slide, it's "amazon-dynamodb-tools" in the repo under AWS Labs. You can actually point this against your AWS account and so long as this utility is given permissions via IAM, it can go take the table name of every DynamoDB table in that region or account and tag it with that table name. So it would kind of effectively do the same as you see above—we found a table named "tweets" and we added the tag "table name: tweets".

**Greg:**  
So this is a great way if you've got some of this quick Cost Explorer tagging filter capability but you haven't tagged any of your tables—we can kind of let this tagger utility go handle a large number of tables and then you get that resource on filtering in Cost Explorer real quick.

**Greg:**  
So now that we have all of our tables tagged, let's say we found at least like a top table that's contributing to our bill. So we've done that filtering in Cost Explorer to see where our usage is coming from—we found the "tweets" table. Now we want to go look into that specific table and understand maybe whether there's something we can do differently about how we've configured it.

**Greg:**  
So the first option we're going to look at is actually choosing the right capacity mode for our table. In DynamoDB we provide two separate capacity mode options. One is on-demand, which is going to be a pay-as-you-go style capacity where you're not giving us a specific headroom—you just say handle all of my requests, and as long as you have even a fairly spiky workload we can manage that workload on the back end for you and you really don't have to think about capacity. Provisioned is more of a conventional style where you set a specific amount of resources that you want to have available and we will make that amount provisioned on your table and you can go from there.

**Greg:**  
So taking a closer look at on-demand—this graph on the left is a really great example of an on-demand workload where we have large spikes of traffic that sort of are random. There doesn't seem to be a particular rhythm to them—you may occasionally drop down to zero traffic, maybe on the weekend no one uses the service. We don't necessarily want to pay for a database that's sitting idle for the whole weekend.

**Greg:**  
Now because we don't force you to provide a specific number for provisioning here, you don't have to really keep in mind how much capacity you'll need from day to day or hour by hour. We're just gonna kind of roll with that pay-as-you-go model and scale up and down for you behind the scenes. So the benefit here though is when you have traffic spikes you don't have to be aware ahead of time that that spike is coming, and you don't have to have an over-provisioned table just to tolerate that amount of extra traffic.

**Greg:**  
Some things to keep in mind with on-demand: When you create a table, we're going to start with a base throughput of 4,000 WCUs and 24,000 RCUs. So effectively we're creating a set number of partitions behind the scenes to handle your traffic. But what happens over time is as you use this on-demand table, we are always going to add enough extra partitions to be able to scale to twice the previous peak throughput that you've ever driven to the table. So if today you drive 10,000 WCUs to the table, we will make sure there's enough partitions behind the scenes to scale immediately to 20,000.

**Greg:**  
So as your workload grows we're gonna naturally have that headroom built in. Now the cool thing about on-demand is there really is no maximum here—the only limit is just how quickly you beat your previous peak. So we can't necessarily go from 10,000 today to a million in the next hour; there will be some scaling behind the scenes. So we have to make sure that we understand at least some of our workload pattern, but in terms of going to production and day-to-day usage you can expect a nice, carefree operational scaling on the table.

**Greg:**  
Now on the other side of things we have provisioned capacity. Provisioned capacity, as I said, is where you set specific throughput levels on your table. It's more of a “set it and forget it” capacity that you occasionally change based on workload, but we're not really expecting to tolerate significant spikes or changes in the workload. So what we're able to do on provisioned capacity is we set our read and write capacities separately. So maybe you have a table that has a lot of write throughput but almost no reads—or vice versa—we can tune those independently to make sure we're not overpaying for one or the other.

**Greg:**  
Now one of the benefits of provisioned capacity is if you have a very steady workload—where you have like a predictable ramp up maybe in the morning or a specific time of day and it gradually builds up and then it comes back down at night—this can actually be more cost efficient than on-demand. But with that predictability, on-demand is built to tolerate unpredictability. So if we have unpredictability in a provisioned capacity table, it is possible to have throttling—and throttling really means that you thought you needed 10,000 writes and all of a sudden you needed 20,000 for an hour. Well, we have to be able to scale up to meet that. If the scaling is not able to happen quick enough, we're gonna tell your client, "Okay, we're throttling you—you need to cool it down a little bit and then come back for another attempt later."

**Greg:**  
So the challenge here with provisioned capacity is we also don't want to over provision. If we set these throughput levels too high but then we only use a fraction of them, we're effectively wasting money because we've provisioned for a peak that didn't happen.

**Greg:**  
So with auto scaling we can actually set specific targets as well as minimums and maximums, and what auto scaling is going to do is try and follow the curve of your traffic on the table. So you see here in the console we can turn on auto scaling and set minimums and maximums. Think of those as just sort of billing and throttling protection: the minimum capacity units is almost more of a “I want to prevent throttling by keeping this amount of capacity available,” and maximum is “I want to prevent runaway billing in case something goes wrong with a new code release.” But ultimately, those are just guard rails. Target utilization is where you really want to focus your efforts for cost optimization because what target utilization tells us is how much of this headroom to always keep on your table. In the instance of this, with 70% target utilization there should almost always be 30% of overhead capacity sitting and ready for a short-term spike. Beyond that 70%, if you make a higher target utilization number, that means there's going to be less headroom—more chance of throttling—but you're also leaving less capacity on the table when it comes to actual consumption. If you lower that number, you're going to be increasing your bill versus actual traffic but you're avoiding throttling. So this is a good number to play with to figure out what your comfort zone is between throttling and cost efficiency.

**Greg:**  
So now if we look at auto scaling in action—here we can see these two graphs. The one on the left is for reads; on the right is for writes. The blue line is what's been provisioned on these tables and the orange line is what we saw actually consumed. So we can see auto scaling kind of flowing with that uptick in what looks like the morning and then gradually scaling back down overnight. But then the next morning you could see it come right back up and toe that line. So if we think of a more instance-based database, we would probably provision a certain number of instances for peak—so maybe in this example on the left we would set a peak at 60,000. If you envision a line at 60,000 and then take the difference between that 60,000 line and the blue line—that's money that auto scaling has saved you. So it's very effective at following those sort of steady and predictable workloads and saving you money over the course of a given day, because we can't have a human constantly looking at this.

**Greg:**  
Now behind the scenes auto scaling is actually built on CloudWatch. So when we create a table with auto scaling, we're actually going to make a CloudWatch alarm that is tracking the metrics of the table. So what's happening is CloudWatch is constantly looking at these metrics, taking a look at the target utilization of the table, so it applies that target utilization percentage math against what the current metrics are, and it figures out whether—based on the last two minutes of traffic—whether it needs to scale up, and then if it does, what it's going to do is call the AWS auto scaling service, trigger that auto scaling event, and the auto scaling service talks to DynamoDB to actually update that table's capacity on your behalf.

**Greg:**  
So there is obviously some delay here. This is an asynchronous process. So this is really where choosing between on-demand and provisioned capacity comes into play because provisioned with auto scaling has this sort of a little bit of a delay to it. So if you have a spike that lasts only maybe a minute or so, auto scaling isn't going to be able to help. If you have this spike where maybe you're ingesting a large amount of data and you expect it to last an hour, auto scaling will eventually catch up to that traffic and it will get the table in the right spot. We'll talk a bit later about how to handle large data loads in an effective way while still using auto scaling though.

**Greg:**  
Now, another thing to keep in mind with capacity on DynamoDB tables is we do have the concept of burst capacity. So sudden spikes do happen—we fully understand that—we're not going to immediately throttle a table just because for one moment you went over your provisioned capacity. We actually keep buckets with five minutes of capacity available for your table. So assuming you haven't used more capacity than you provisioned for the last five minutes, you have five minutes of that capacity available in the bucket. So you can see in this chart the table was provisioned at, say, five capacity units, and we have a couple of spikes that actually go around 10 to 25 momentarily, but we don't actually see throttling on this table because they're short-term spikes and they use that burst capacity bucket while we have it.

**Greg:**  
So while there may be some situations where it looks like auto scaling can't keep up with spikes on your table, sometimes we can also just tolerate these spikes with burst capacity and we don't have to go to on-demand just because the spikes exist. What we need to keep an eye out for though is sustained traffic above provisioned levels. If you are consistently needing five times your table capacity for the first minute of every hour, that's probably not going to work very well in the long run for auto scaling or provisioned capacity. I'd suggest we start looking into on-demand.

**Greg:**  
So a lot of people will say provisioned capacity is always cheaper than on-demand, or they look at the way things are billed and they'll say it's 80% cheaper. Is this true? Now, for a consistent, flat steady workload with a perfectly provisioned capacity, let's imagine a table that uses 10 WCUs all day, every hour of the day—yeah, provisioned capacity would be 80% cheaper. On-demand effectively ends up at roughly five times the cost in that perspective. But once some variability and unpredictability comes into the workload, you will always have some level of over provisioning on a provisioned capacity table. It's unavoidable, and let's be honest, every real world database is going to have variability in its traffic. I'm sure we all wish that we could have a perfectly flat workload, but it's just not how it works.

**Greg:**  
So there becomes a bit of a decision point here where we have to figure out where our traffic lies between a flat and steady workload and a spiky workload. So what we want to do is we want to start looking at our CloudWatch charts for the table—now we look at those throughput consumption graphs, so write capacity units and read capacity units—we want to look at what the throughput usage on the table is.

**Greg:**  
Now, if I'm looking at a table that has on-demand capacity, I want to look for tall spikes and potentially drops back to zero. If we have a chart like that example for on-demand earlier on, where we have points in the day where nothing gets used or traffic goes from maybe 10 to a thousand WCUs in moments, that's a really great candidate for on-demand and it will likely be cheaper.

**Greg:**  
Now if we see a table with steady traffic—that kind of is more of a sine wave, just nice consistent growth and regression on the throughput—we should probably look into moving that into provisioned capacity. We still want to look out for those tall spikes though, just because we can see that 99% of the day it's consistent, we can't ignore the fact that maybe for parts of the day there's some spikiness.

**Greg:**  
Now for a table that's currently in provisioned capacity—like kind of the inverse here—we want to make sure there's no tall spikes that are causing throttling. We have another CloudWatch metric for you to look at, that's throttling events. So if you start seeing throttling on your table, we either need to look at raising the capacity with auto scaling on that table or potentially moving it to on-demand because the workloads become more spiky than we expected.

**Greg:**  
We also want to look for gaps in that usage. If we start seeing situations where the table is just unused for periods of time—particularly an hour or two—that's still a good candidate for on-demand.

**Greg:**  
If you're still seeing throttling while having enough provisioned capacity on the table, there's another aspect here that we want to keep in mind: it is possible to have throttling at the partition level, which would be based on having a hot key. So maybe a given partition key is more actively used than you expected. This is getting more into some schema-level redesign, but we suggest that if you go take a look at CloudWatch Contributor Insights—this is a newer launch of ours where once you enable it for a table, it will actually tell you what your most actively used partitions and keys are on the table. So maybe you can trace down who's contributing to these throttles and take care of that from a data perspective. But at the table level, you can at least be aware that you've scaled the table to an adequate capacity.

**Greg:**  
Now on provisioned capacity we also want to take a look at whether there's bulk loads that exceed these thousands of ECUs that can also be contributing to throttling. So maybe we take a look into breaking that bulk load out into a longer period of time or multiple partition keys.

**Greg:**  
All right, so next we're going to take a look through a few examples of tables and kind of explain from a metrics perspective why they're either in a good or bad capacity.

**Greg:**  
So this example here we have a provisioned table and it has auto scaling enabled. We can see that there's a fair bit of headroom for most of the table or for most of the day—it looks like we're probably at something like a 50% or 60% target threshold. So we have a bit of wasted capacity, but it's following the relatively steady curve of the graph fairly well. You can see there's just a bit of spikiness on the consumption—though it's not too steady, like we're kind of bouncing back and forth by about 20 to 40% at a given time.

**Greg:**  
Now, I think this is a good one to keep in auto scaling and provisioned capacity. The one thing that kind of can give some people pause is on the right, you see the orange approaches the blue a little close. Now I think what happens here is for that momentary bit—that's perfectly fine. If we see that happening too frequently, I'd get a little concerned and maybe look into changing that target threshold. But I think we're in a good place here—we're not wasting too much provisioned capacity and the consumption is staying relatively far enough away from the provisioned.

**Greg:**  
Now this next one is a little different. We see that this is still a provisioned capacity table, but this consumption is actually getting really close to or potentially exceeding the provisioned capacity. So we can almost expect here that we're using parts of our burst bucket to handle some of these spikes. But for the most part, the blue line is keeping over the orange line so our provisioned capacity is on the whole adequate. This is a bit more of a gray area here, I think—we could probably try this table out on on-demand and see how the bill changes. Maybe it'll go down; it's probably going to be pretty close to the same. But what we want to keep an eye out for, particularly here, is—let's go look at the throttling events on this table. If we're getting a lot of throttles, we should probably try and raise, or we should probably try and change that target threshold to have a little more overhead. We might be able to absorb some of these spikes a little better and avoid some throttles. But the more we do that, the closer we get to on-demand being a better candidate. So this one's kind of a no-good answer situation and we kind of want to take a look at both options as we go. Remember that you can change back and forth between on-demand and provisioned capacity once per day—so you can give it a try for a given day and then change it back the next if it didn't look like it affected the bill in a good way.

**Greg:**  
Now this last one should be pretty clear. This is a very spiky workload—we fall back to zero traffic pretty regularly. That spike isn't happening at a predictable part of the hour or it's not very long; it's a pretty short spike. So this is a really great candidate for on-demand here. The provisioned capacity would really not be able to help us much here—we'd be over provisioning by quite a large margin.

**Greg:**  
All right, so thanks. 

---

**Julie:**  
Hi everyone, I'm Julie, our DynamoDB specialist solutions architect at AWS. And let's start with the next part of this webinar today by diving into the table classes.

**Julie:**  
So we've always had this standard table class which balances the costs of storage and throughput. But recently we announced a new table class called the Standard Infrequent Access. It is basically for workloads where storage is a dominant cost. It reduces your storage cost by around 60% and it provides the same performance for your reads and writes. The throughput costs are approximately 25% higher with this table class, so it is essentially suitable for use cases where you write to a table—making it storage heavy—but then you do not access it very frequently. So something like time series data or log metadata, for instance.

**Julie:**  
So apart from your understanding of the use case, a general guideline to identify candidates for the Standard IA class is that the storage costs for the table exceed 50% of the total throughput costs for the table.

**Julie:**  
So the choice of table class affects a few pricing dimensions. For example, the throughput costs for local and global tables and also the storage costs—which are basically going to reduce—it affects your GSI costs since GSIs inherit the table class from their parent, right? And then this is an important consideration because if you have a table that you write a lot to but you don't touch the table, however, you are actually reading from the GSI heavily, then maybe it's going to affect the choice and the calculation because the GSI throughput is going to be charged based on the new Infrequent Access table class, right? And then additionally, reserved capacity is not supported with this Standard IA class. So if you are relying heavily on reserved capacity, we might need to rethink the choice and the calculations.

**Julie:**  
So what you would basically do is to calculate the storage and throughput costs for each table and share size, and then see if it meets the criteria of storage costs being greater than 50% of the throughput costs.

**Julie:**  
So based on different throughput modes, the read/write calculations can differ. Greg walked you through the provisioned mode and the on-demand mode, so basically with provisioned mode it's fairly easy to plug in your RCU/WCU values, multiply them out with the costs, and compare them, right? So you basically know that one is higher than the other. But it's important to keep in mind that if your table has a lot of auto scaling and if you're doing instantaneous calculations at a given point of time, then your comparisons might not be valid anymore.

**Julie:**  
So it is important to take all the auto scaling activity into account when you are actually doing all these calculations. With on-demand mode, you want to look at your consumed capacity history in CloudWatch to figure out the throughput costs. So we do not have a CloudWatch metric for the storage unfortunately, but with the capacity metrics you get an idea of the capacity costs; and for storage, what you basically do is either look at the instantaneous values by using the CLI or console, or it basically will help you figure out how big a table is right now, and then you do manual growth estimates—something like if you think your data is going to grow by 20% a month, so factor that growth into your calculations and see what your projected table costs are going to be.

**Julie:**  
So as mentioned earlier, the table class also affects global tables. So if you are using global tables, tables in different regions can have different table classes. So depending on if you have one region that's being read or written to heavily while the other not so much, you can decide whether the one that's not read as much can be switched to Standard IA or not.

**Julie:**  
And then it is important to take all these points into consideration—about the auto scaling, about the GSIs, and about the global tables—so that we don't arrive at incorrect answers from our calculations.

**Julie:**  
So we have come up with some tools to give you an easier starting point. This tool is called the Table Class Evaluator. It is essentially written in Python and it can be run from the command line. So it is intended to run automatically every week or so. You can basically have something like a scheduled Lambda, for example, which will run this every week. And what the tool does is it will look at every single table in a region and it will call APIs to describe those tables, any GSIs on those tables, and it also considers global table replicas so that it can use the correct pricing for global table usage applicable.

**Julie:**  
The tool performs calculations for both classes and it will recommend you to change the table class for a table which might do better with Standard IA. So the tool does have some limitations today and it is still a work in progress. As of today, it works for tables that use provisioned capacity only. If you have some tables in the region that are using on-demand capacity, the tool might not work for you yet; and if you have a lot of auto scaling activity as well, the tool only calculates based on when you run it. So if you happen to run the tool and get a recommendation at a period of exceptionally low utilization and then auto scaling bumps—and then you have a lot of utilization after you've actually used the tool—the results could be incorrect.

**Julie:**  
And like I said, it's a starting point to make it easier. We're still working on the tool. I'd say use the tool in the context of looking at the CloudWatch metrics history, and also that as of now the tool does not consider LSIs. So if you have any local secondary indexes, please do consider them in your calculations.

**Julie:**  
So you can find this tool at the GitHub repo that's right here below. You can see it sits in the AWS Labs repository—it's open source, approved and released as an official Amazon tool. So go ahead and explore it.

**Julie:**  
So one more thing to mention here is that you can switch between the table classes twice every 30 days. So that means if you actually use the Standard IA and find that your table might do better or your throughput consumption has increased, you can go back to using the standard class.

**Julie:**  
So moving on from table classes, look at these interesting CloudWatch metrics trends here. So they basically indicate that the GSI is unused. But wait, how? We do see activity in the write metrics on the right-hand side, right? So how can we call it unused? The point I'm trying to make here is that writes are being propagated from the base table and we're actually consuming write capacity on the GSI, but there is no read activity to justify the existence of this GSI. So you create a GSI because you want to look up your data by a different criteria. So it is possible that your access patterns have changed or the GSI was created with something in mind but it's just sitting there not being read right now. It's basically consuming your storage, it is consuming your write cost to propagate writes from the base table, but you're not actually reading from the GSI. So it is important to monitor the GSIs and delete them if they are not needed.

**Julie:**  
Similarly, you can have CloudWatch alarms on such metrics to see if your consumption falls to zero or an exceptionally low value for a period of time—say 30 days or so—for your GSIs and for tables, so that gives you a better idea of if you have a lot of unused tables and GSIs in your account, and getting rid of them can probably save you on costs.

**Julie:**  
There are some suboptimal table usage patterns that we see frequently and they might be worth digging into for today's discussion. So the first one is where customers only use strongly consistent reads. So DynamoDB considers read requests as eventually consistent by default. That means if you don't pass any consistency parameters with your requests, they are going to be treated as eventually consistent. It basically means that you could see stale data depending on how long the replication time is between your write and the moment when you actually issue the read request.

**Julie:**  
So we charge eventually consistent reads at half an RCU for up to 4 KB of data. That means you can read 8 KB of data with one RCU in an eventually consistent manner. That being said, many customers have a part of the workload that requires strongly consistent reads or read-after-write consistency, as some may call it. So we do provide strongly consistent reads with DynamoDB, but it varies in charge—basically we charge you one RCU (or read capacity unit) to read up to 4 KB of data. So essentially, it's twice as expensive as an eventually consistent read.

**Julie:**  
So what we observe is that instead of using strongly consistent reads only for the part of the workload where customers actually need it, they end up changing the entire processing to use strongly consistent reads. So this, of course, doubles up the DynamoDB read costs unintentionally when you could have actually gone with maybe 10 strongly consistent reads where you actually need that read-after-write consistency.

**Julie:**  
And then if you're seeing high read costs and that's a concern, then it's important to talk to your developers and get your code reviewed to confirm if this is indeed the case at hand.

**Julie:**  
Similarly, we have some customers performing all operations as transactions. DynamoDB allows you to group certain actions in an all-or-nothing fashion. So for customers who come to DynamoDB—especially from the relational background—they're used to wrapping every operation in a transaction for safety. So while it is very common and one of the best practices with relational databases, it need not be the case with DynamoDB. So use transactions only if absolutely needed, since it has obvious cost implications. A transactional read of up to 4 KB consumes two RCUs as opposed to the default 0.5 RCUs for eventual consistency. So the costs are doubled in case of writes—which means a transactional rate of up to 1 KB equates to 2 WCUs.

**Julie:**  
So this case is relatively easier to identify. You can check your CloudWatch metrics, filter them down to the transaction APIs, and see if the overall capacity consumption trend matches exactly without transaction API usage—or just see if transaction APIs are the only graphs available for your table. This would confirm that everything is done as a transaction for your table, and it is worth justifying if everything actually needs to be a transaction or given the extra costs that come with transactions.

**Julie:**  
The next pattern that we'll talk about is the extensive use of scans. A lot of customers want to be able to run analytical queries on their DynamoDB data, but because DynamoDB is not an analytical database, people say, "That's no problem, we'll just run a scan, we'll get the entire data dump and then we'll create analytical outputs on top of it." However, it is worth taking into account that scans can be quite expensive, since we charge you for the amount of data read—the filter conditions, if any, are applied on the data only after the data is read. So a better alternative to repetitive scans is the "Exports to S3" feature. It allows you to choose a point in time to export data to S3, and it's available in a couple of formats. So it becomes easier for you to run analytical queries on the S3 data, and at the same time it does not consume any capacity from your table.

**Julie:**  
The feature does require you to enable point-in-time recovery and it incurs costs, but if you look at CloudWatch and see that scans are very frequent, you need to re-evaluate why there are so many scans and probably have a deeper discussion on the way that you are actually accessing data—and if exporting to S3 for a periodic analysis is a better option cost-wise and performance-wise.

**Julie:**  
Next, on or not using TTL is another pattern that we've seen often. So using TTL requires you to have a field in each of your DynamoDB items formatted in a certain way. So for already existing workloads, TTL can identify items which are older than the expiry time that you have set for that item, and then once the time is up, the item is cleaned from the table. So TTL trims your data down and helps you save on storage costs, and another useful aspect—or the most useful aspect of TTL—is that the expired item deletion itself does not cost you anything. Removing the items via TTL is free, and the item deletions also occur as stream events. So if you have a DynamoDB stream enabled on your table, you can consume from the stream and maybe archive the data or store it in S3 for certain analytical purposes. So instead of using DeleteItem calls to clean your older data, use TTL.

**Julie:**  
And it basically will save you on storage costs and the DeleteItem call costs.

**Julie:**  
One more thing under consideration is your backup settings or backup strategies. So DynamoDB backups can now happen in two ways. When we say backups, it's the on-demand backups that we're talking about and not the point-in-time restore. So the built-in DynamoDB backup allows you on-demand backups, and the second way of actually going about your backups is using the AWS Backup service. Using the service is better because it comes with a lot of extra features. The most important feature from the cost optimization front is the tiered storage. It basically allows you to move your backups to a colder storage as per configuration, and the colder storage tier is significantly less expensive than the hot storage. So you can configure these settings and also choose retention periods for your backups.

**Julie:**  
So the backups in AWS Backup also inherit the tags from their tables. So if you have tagged your tables as we talked about earlier, you can do some cost optimization or cost allocation analysis for your backups as well. And an opt-in is required to use these features with AWS Backup to manage DynamoDB backups, and it should be available in both the AWS Backup and DynamoDB consoles.

**Julie:**  
Another good reason to use AWS Backup has to do with global tables. So global tables is this awesome feature that allows you to maintain multiple active replicas in different regions. What I mean by active replicas is that all of them can accept writes at the same time and replicate data across each other, so it is easy to set up replicas and the sync across them is managed for you. The replicas eventually converge to a consistent state using a last-writer-wins strategy. So in essence, global tables is a great feature for workloads that actually need it, but we've seen that customers use global tables as a part of their disaster recovery strategy. So if you have relatively lenient RTO or RPO objectives (recovery point objective and recovery time objective), then global tables might not be the best way to look at it because it comes with the cost for replicated WCUs, right? So an easier way to take care of your DR, or relatively lenient DR—something like a few hours or 12 hours or a day—can be easily managed with the cross-region backup copy feature provided by AWS Backup. So that way it's going to be costing you less, and you're not essentially using global tables for disaster recovery in that case.

**Julie:**  
So this is another feature that we launched around re:Invent 2021. It allows you to filter DynamoDB stream events for AWS Lambda. So if you're familiar with streams, they contain an event corresponding to each data modification on the table. So when you insert an item on the table, or update or delete for that matter, the record of each of these changes is going to be present in the stream. So AWS Lambda is one of the most common consumers of the stream that can be configured, and customers use this pattern very commonly for something like near real-time processing.

**Julie:**  
So basically if you have a Lambda which is subscribed to a stream, it gets triggered on every single event by default. And this was the behavior until recently—basically you had to take the event filtering or evaluation logic into account on the Lambda code end. For example, if you want to skip the delete events, your Lambda logic needed to identify the deletes and then just return without doing anything. So this led to something like wasted utilization for that trigger because your Lambda is running but it's doing nothing—it's just evaluating the kind of event.

**Julie:**  
So what this new feature does is it allows you to add event filters so the filters decide what triggers a Lambda function. So you can decide the events of interest for actually triggering your Lambda. The filter could be the type of event, which is, for example, identifying the event name in the DynamoDB stream, and with filters you could say, "I only ever want to see new inserts" or "don't show me any modifications," or, you know, things like partition keys. If there are certain items that interest you, then you can choose to filter the events, or depending on the partition key value as well.

**Julie:**  
So almost anything that you can think of that will be exposed in the stream is what you can base your filter on or compose your filter on. So let me show you an example of how you do this. On the left you can see that we have an example of an abbreviated event in a DynamoDB stream, and in this event I have a partition key of a string type identified by the "S" that you see there. And then I want to process any event that comes through for a particular actor, but I don't necessarily need it for a particular movie—I am interested in all movies by that actor. So the filter pattern that I configure on the right, as you can see, is that I provide a prefix with some actor. So whenever my key has that actor as a prefix, the function is going to trigger, but other functions or other changes are not going to trigger my Lambda function. So you would define these filters using JSON syntax, as you can see below, and the Lambda is going to do its job without you having to take care of the evaluation logic or to identify the events of interest inside the Lambda code itself.

**Julie:**  
An interesting thing to note about this cost optimization recommendation is that it doesn't actually save you any costs from the DynamoDB end. So this basically means that the GetRecord calls are already free, right? So if Lambda is your consumer, you don't get charged for the GetRecord calls. So if it's not going to save your DynamoDB cost, why is this even a recommendation? The reason is that it saves you a lot of money potentially from the Lambda invocation costs, and we see many customers using DynamoDB streams to Lambda as a pattern to address a large number of use cases. So that's how the wasted utilization that we talked about earlier can be eliminated and the Lambda computation costs can be saved.

**Julie:**  
So we also have a limitation here: you can have up to five filters on a single DynamoDB stream and it's a soft limit—you can have it increased to 10, which is a hard limit. And the filtering occurs in an OR fashion, which means if any of your events matches any of those filters that you have configured, it is going to be passed through.

**Julie:**  
So we are now opening the floor for questions. Keep them coming.

[Music]