# online-retail


## 1. 🛠️ Installing Poetry

To install [Poetry](https://python-poetry.org/) (Python dependency management and packaging tool), run the following command in your terminal:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

After installation, make sure Poetry is in your `PATH`
- macOS/Linux
```bash
export PATH="$HOME/.local/bin:$PATH
```

Verify installation:

```bash
poetry version
```

Keep venv inside the project (works great with VS Code) poetry 

```bash
config virtualenvs.in-project true
```
This environment is set with Python 3.13. Change the requires-python = ">=3.13" in pyproject.tmol file if you have other versions on your PC.

run:
```bash
poetry install
```

In case if you want to make environment from scratch, run:(Do not recommended)

```bash
poetry new project_name
```
## 2. Source of Data

Data is in `data` folder, but you can download from:
[Kaggle Link](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset/data)

## 3. Exploratory Data Analysis (EDA)

`src/online_retail/EDA.ipynb`

Explanation of this section is in the notebook file. Install data wrangler in VSCode for having better experience. In this file, I did Exploratory Data Analysis (EDA), which is RMF analysis. RMF analysis is:<br>
R -> Recency: How recently a customer made their last purchase -> more engaged and more likely to buy again.<br>
F -> Frequecy: How often a customer purchase -> Loyal customers.<br>
M -> Monetary: How much they spent -> spend a lot have more value.<br>
This is a study that is used for customer segmentation technique. RFM is a `KPI` to segment the customers. The goal is to quantify customer value and behavior. So using these three criteria, we can segment our customers into 5 categories.<br>
1. Champions -> High RFM -> loyal and active.<br>
2. Loyal -> High F but regular M -> Regular customer.<br>
3. Big Spenders -> High M low F -> High value but occasional<br>
4. At Risk -> Used to buy but not now -> At risk for churn<br>
5. Lost -> Have not purchased for a long time.<br>

At the end, I generated a clean table, that contain RMF columns, and score each customer using RMF features. Based on the histogram analysis, Recency has exponential distribution `log(y)=mx+b`, Monetry has log-normal distribution `log(x) ~ N`, and Frequency has power-law distribution `log(y) = mlog(x)+b`. The correlation analysis shows there is a Positive correlation ($\rho = 0.65$) between Monetary and the frequency. It is evident in Fig1. as well.


Fig 1: Joint scatter plot of Monetray and Frequency.<br>

<img src="Fig/Mon-Frq.png" alt="jdist-mon" width="400"/><br>


## 4. Customer segmentation

`src/online_retail/cust_seg.ipynb`

Next, we want to segment our customers into 5 different groups `[Champions, Loyal, Big Spenders, At Risk, Lost]`. To do so, I give a score to each customer for each RMF feature based on quantile analysis. Customers with `R_score >= 4, F_score >= 4, M_score >= 4` are `Champions`. Customers with `R_score >= 3, F_score >= 4` are `Loyal`. Customers with `M_score >= 4` are `Big Spenders`. Customers with `R_score <= 2, F_score >= 3` are `At Risk`. Customers with `R_score <= 2, F_score <= 2` are `Lost`. `Need Attention` customers could be new customer who have high `R_score`, but low to mid `F_score`, and `M_Score`(i.e., averagly they just had 1.7 transaction within the last 32 days). The figure below shows a bar plot of the average KPIs for different customer segments.

<img src="Fig/KPIs_barplot-1.png" alt="KPIs" width="400"/><br>

## 5. A/B testing

Since 867 people are in lost group, one of the interesting tests we can do is the following:
How much discount should we offer the lost group to revive 20% of them with a probability of 90%?

“Customers who spend more always remain our customers, so we can offer promo codes to other customers to increase revenue.”

### process for A/B testing
- Hypothesis of A/B testing:
Bussiness hypothesis describe what two product are being compared and what is the desired impact on the product. In this step we should consider what issue we want to fix and which KPI should be tracked to see the influence of the changes in the product. Single Primary Metric should be used to evluate the results of the A/B testing, whether statistic of the control group (Old version of the product) and treatment group (new version of the product) are significantly different or not.
For choosing the Metric, we should always answer this question: By keep all parameters constant and chosing the Metric, would we achieve our goal? like conversion rate or click through rate(CTR)
What metric we should use here?
Then we need to bring up hypothesis testing (H0, Ha)
- Design A/B testing:
1. Power analysis:<br>
FP: The probability of rejecting the null hypothesis when it true(Significance level(type I error): $\alpha$). This is the risk that we take to reject the H0 when it is actually true. This values is used to calculate the Confidence Interval(CI).<br>
FN: The probability of rejecting the alternative hypothesis when it is true (tyep II error: $\beta$). This is also a risk we take to reject the H1 when it is actually true. We use $\beta$ when we want to find minimum sample size. This parameter is not used for statistical analysis.<br>
TP: The probability of rejecting the null hypothesis when it is wrong(Power = 1- $\beta$)<br>
TN: The probability of rejecting the alternative hypothesis when it is wrong (Confidence level= 1-$\alpha$). This probability is used to analyze the CI. If with high probability (1-$\alpha$) the CI covers a narrow range, we can confidently conclude the test with high accuracy.<br>
P: rejection of H0 or approval of H1.<br>
N: approval of H0 or rejection of H1.<br>
Basically, we always take two risks $\alpha$ and $\beta$. If we want to be conservative, support H0 more than H1, we choose $\alpha$ less than $\beta$.
- Choosing the probability of correctly rejecting the null hypothesis (TP = 1-$\beta$) in which $\beta$ is type II error(FN the probability of failing to accept the alternative hypothesis when it is true). It is common to choose power = 80%. We are ok with failing to reject the null hypothesis when it is wrong 20 percent of times.
- Significance level ($\alpha$): The probability of rejecting the null hypothesis while it is true(type I error or FP). When $\alpha = 0.05$ there is 5 percent change of concluding that there is significance difference between control and treatment group when there is no actual difference. If the implementation of the new model is expensive, we should choose smaller $\alpha$ to reject the null hypothesis harder, unless there is significance difference between treatment and control.
- Minimum Detectable Effect (MDE) or $\delta$: What is the minimum amount of change we aim to observe in the new version to lunch the new version. There is no normal amount that can be considered and usually it is determined by stakeholders. it can be 1% for one product and 5% for another product. This variable is used for computing practical significance. If MDE be less than the lower bound of the CI, we can say the model is practically significant.
2. Minimum Sample Size: To avoid bias results, we need to determine minumum number of samples that we should take out of the population. H0: $\mu$ control = $\mu$ treatment. H1: $\mu$ control is not equal to $\mu$ treatment. or for our case H0: the monetray of top 20% customers is not equal to the monetray of same customers in year2. H1: the monetray of top 20% customers is equal to the monetray of same customers in year2.
Based on CLT, the distribution of the mean of the sample follows the normal distribution. So $\bar{X_{con}} = N(\mu_{con}, \sigma_{con})$ , $\bar{X}_{exp} = N(\mu_{exp}, \sigma_{exp})$, $\bar{X}_{con} - \bar{X}_{exp} = N(\mu_{con}-\mu_{exp}, \sigma_{con}^2/N_{con}+\sigma_{exp}^2/N_{exp})$
N = ($\sigma_{con}^{2}+\sigma_{exp}^{2}$)$(z_{1-\alpha/2}+z_{1-\beta})^{2}$/$\delta^{2}$ derived based on AA testing. As the risks we are taking increases, $\alpha$ and $\beta$, the number of samples needed for the test reduces. If MDE be small, then we need more samples to detect the rise in the outcome.
3. Test duration: N/(average # of visitors per day) considers the factors like Christmas can affect the number of visitors of the page. So do not run the experiment in those days which result into inaccurate conclusion.
Too small test duration result into novelty effect. Users tend to react quickly to a new platform which is considered illusionary. 
Too long test duration result into maturation effect in which the test is affected by the external parameters. 
_ If the test is statistically and practically significant and the CI is narrow, it shows the test is performed accurately, and precision is high, and we can generalize the test.


## 6. Causal inference
For the causal inference also we need to have treatment and control group. However, the test is not run in randomized way and we need to use previous experimental data(test can not be re run). Not randomizing the samples to control and treatment group my causes biased result and confonded by other parameters. In causal inference we are trying to infere by removing the effect of the confond parameters which comes from not randomized controled test(RCT).