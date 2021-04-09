# How many trawls do we need to sample to make sure we can detect a biologically important effect?

## Background
One of the problems with data in general, and ecological data in particular, is the samples are variable in time and space. In fish trawls, for example, we can get skunked, gazillions of fish, or anywhere in between. Whenever we refer to a value - for example fish per haul - we will also have a measure of the variability of this estimate. Commonly this measure will be the standard deviation, which is the average difference between each individual sample, and the overall mean. You may also see the variance (the standard deviation squared), or standard error (the standard deviation divided by the square root of the number of samples).  

In formal literature, we may see this stated as a problem of statistical power. In basic terms, this is the probability of finding a difference between sets of samples if it in fact exists. Personally, I don’t buy into the formal power analysis side of things for various technical reasons. The solution is actually far simpler.  

Enough of the eye-glazing part, let’s get a better feel for this. Cosgrove et al. 2019 (https://www.sciencedirect.com/science/article/pii/S0165783618302558?via%3Dihub) provide some individual tow data examining Nephrops/finfish separation methods in the Celtic sea. Let’s have a quick look at the Haddock & Whiting abundances:  

```{figure} RawHaddockWhiting.png
:height: 300px
:align: center
```

As a heads-up on boxplots, the box represents the 25th and 75th percentiles (the bulk of the samples, in other words). The line in the middle is the median or center of all the values, and the whiskers are 5% and 95% percentiles.

What do we get from this plot? Haddock catches can be consistently low, with occasional big hits. Whiting is also pretty variable, but we don’t get the skewed pattern in Haddock. This symmetry is actually good for analysis. 
In the case of Haddock, we can make the distribution more symmetrical by transforming it. For example, a log<sub>10</sub> transform:  

```{figure} LogHaddockWhiting.png
:height: 300px
:align: center
```

Well, that fixed Haddock but screwed up Whiting and make it right-skewed. For this data set, log transform Haddock, but leave Whiting as is.  

An aside... What does the logarithm (in this case, base 10) actually mean? The scale is actually quite intuitive. log10(1) = 0; log10(10) = 1; log10(100) = 2; log10(1000) = 3; log10(10000) = 4 and so on. Think one, a few, some, a fair amount, lots, buttloads.  

Why is this important to us? If we need to get trawlermen to count fishes, they can classify them into tractable defined groups which is easier and foolproof for them. For the analyst, the data can be treated as linear, on a logarithmic scale.  

Back to the problem...  
Let’s focus on Whiting. We can work on the raw data scale and omit one level of magic. Here is a simple plot of the Whiting data including the zero value (I omitted it above for comparison) and all I have done is repeated the data, but shifted the mean value. So, same values with an arbitrary amount say, 25% & 50% subtracted from the data copy:  
```{figure} RawSimulatedChange.png
:height: 300px
:align: center
```

Now we see what the problem is with sample variation. There is no statistically significant difference (p 0.08: close to 0.05 though) in the 25% bycatch reduction treatment. Remember, these are just the original data multiplied by 0.75. 50% reduction is looking a bit better. Visually, we are looking at the degree of overlap in the boxes.  

This sample was based on 13 trawls. It looks like for Whiting, we could reasonably expect to detect to detect a 50% reduction with this number of trawls. Think to the Golden Ray trial. We hope to do 15 replicates of each of light on vs off. So this is looking promising.  

What happens if we bump up replication? We can do this by simulating a given average and standard deviation, based on the observed values.  
In this case I used the observed values and simulated a lognormal distribution (I have to do it this way to avoid zero predicted values.  
Compare 10 trawls (p< 0.167 ie. Not statistically significant)

```{figure} LogNormsSimulatedChange10Reps.png
:height: 300px
:align: center
```

Now what if we had sampled 15 trawls in each treatment? p< 0.0028 ie. statistically significant...

```{figure} LogNormsSimulatedChange15Reps.png
:height: 300px
:align: center
```

Exactly the same sample variance, exactly the same difference in mean value - with a difference of only 5 replicates per treatment in each of the sample programs.

## Take home message
It’s not worth scrimping on numbers of replicates to do more (say) gear or light sequences changes on a trip. I’m reasonably sure based on this single data set that we are in the right ballpark of replicates. 20 per treatment would be more convincing, but >30 is overkill.  

We can check during any trip how the data are looking simply by plotting the data with each tow. If there are outrageous spreads of values, if we can do more tows using the same set up then we can do that. If we get lots of values, and there’s still no difference, then obviously that setup isn’t working. Onto plan B.  

```{tip} So what can we take home from this little foray?
Quick and dirty graphs give us our primary insight into adequacy of sampling. This can be used in the field to guide sampling.
```
