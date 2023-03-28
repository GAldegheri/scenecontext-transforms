import pandas as pd
import numpy as np
from sklearn.utils import Bunch
from glob import glob
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import pingouin as pg
from math import ceil
from scipy.stats import binom_test, norm
from itertools import product
import os

# --------------------------------------------------------------------------------------------------------

def get_main_exp_data():
    
    allsubjdata = pd.read_csv('data/allsubjdata.csv')
    
    allsubjdata = allsubjdata[(allsubjdata.samediff==True)&
                          (allsubjdata.simpleseq==False)&
                          (allsubjdata.zoomseq==False)&
                          (allsubjdata.task=='rotation')]
    return allsubjdata

# --------------------------------------------------------------------------------------------------------

def get_zoom_exp_data():
    
    allsubjdata = pd.read_csv('data/allsubjdata.csv')
    
    zoomdata = allsubjdata[allsubjdata.zoomseq==True]
    #zoomdata = zoomdata[zoomdata.Date>=20220830]
    
    return zoomdata

# --------------------------------------------------------------------------------------------------------

def get_sanchecks_and_surveys(allsubjdata):
    
    whichsubjs = allsubjdata.subject.unique()
    
    allsanchecks = pd.read_csv('data/allsanchecks.csv')
    allsurveys = pd.read_csv('data/allsurveys.csv')
    
    allsanchecks = allsanchecks[allsanchecks['subject'].isin(whichsubjs)]
    allsurveys = allsurveys[allsurveys['subject'].isin(whichsubjs)]
    
    allsanchecks['prolific_id'] = allsanchecks['prolific_id'].str.strip()
    
    return allsanchecks, allsurveys
    
# --------------------------------------------------------------------------------------------------------

def compute_dprimes(allsubjdata):
    
    datawithdprimes = allsubjdata.copy()
    datawithdprimes['dprime'] = np.nan
    datawithdprimes['criterion'] = np.nan
    
    # Get hits and FAs
    for s in allsubjdata.subject.unique():
        thissubj = allsubjdata[allsubjdata['subject']==s]
        #assert(len(thissubj)==192)
        for e in [0, 1]: # expected, unexpected
            thiscond = thissubj[thissubj['expected']==e]
            n_resp = np.sum(~pd.isna(thiscond.response)) # n. of actually given responses
            # Log-linear correction (Hautus 1995)
            hitP = (len(thiscond[(thiscond.hit==1)&(thiscond['response']=='j')]) + 0.5)/(n_resp + 1)
            faP = (len(thiscond[(thiscond.hit==0)&(thiscond['response']=='j')]) + 0.5)/(n_resp + 1)
            hitZ = norm.ppf(hitP)
            faZ = norm.ppf(faP)
            dprime = hitZ-faZ
            criterion = -(hitZ + faZ)/2
            datawithdprimes.loc[(datawithdprimes.subject==s)&(datawithdprimes.expected==e), 'dprime'] = dprime
            datawithdprimes.loc[(datawithdprimes.subject==s)&(datawithdprimes.expected==e), 'criterion'] = criterion
    
    return datawithdprimes

# --------------------------------------------------------------------------------------------------------

def dprime_across_time(allsubjdata, winsize=24):
    
    dprime_tseries = []
    winno_tseries = []
    crit_tseries = []
    subj_tseries = []
    pexp_tseries = []
    expunexp_tseries = []
    
    for s in allsubjdata.subject.unique():
        thissubj = allsubjdata[allsubjdata['subject']==s]
        assert(len(thissubj)==192)
        assert(thissubj.p_exp.nunique()==1)
        thispexp = thissubj.p_exp.iloc[0]
        for e in [0, 1]:
            thiscond = thissubj[thissubj['expected']==e]
            assert(len(thiscond) in [144, 48, 96])
            for i in range(len(thiscond) - winsize + 1):
                winno_tseries.append(i)
                subj_tseries.append(s)
                pexp_tseries.append(thispexp)
                expunexp_tseries.append(e)
                # Actually compute measures
                thiswindow = thiscond.iloc[i:i + winsize]
                n_resp = np.sum(~pd.isna(thiswindow.response))
                assert(n_resp!=0)
                hitP = (len(thiswindow[(thiswindow.hit==1)&(thiswindow['response']=='j')]) + 0.5)/(n_resp + 1)
                faP = (len(thiswindow[(thiswindow.hit==0)&(thiswindow['response']=='j')]) + 0.5)/(n_resp + 1)
                hitZ = norm.ppf(hitP)
                faZ = norm.ppf(faP)
                dprime = hitZ-faZ
                criterion = -(hitZ + faZ)/2
                dprime_tseries.append(dprime)
                crit_tseries.append(criterion)
                
    tseriesdf = {'p_exp': pexp_tseries, 'expected': expunexp_tseries, 'subject': subj_tseries,
                 'winno': winno_tseries, 'dprime': dprime_tseries, 'criterion': crit_tseries}
    tseriesdf = pd.DataFrame(tseriesdf)
    
    return tseriesdf
                

# --------------------------------------------------------------------------------------------------------

def make_pretty_plot(avgdata, measure='hit', excl=True, rotzoom='rot', fname=None):
    
    assert(measure in ['hit', 'dprime', 'criterion'])
    
    # Get all differences
    alldiffs = []
    for sub in avgdata.subject.unique():
        thisdiff = avgdata[(avgdata.subject==sub)&(avgdata.expected==1)][measure].values[0] - \
                   avgdata[(avgdata.subject==sub)&(avgdata.expected==0)][measure].values[0]
        alldiffs.append(thisdiff)
    alldiffs = pd.DataFrame(alldiffs, columns=['difference'])
    
    fig = plt.figure(figsize=(10,10)) # (10, 8)
    #with sns.axes_style('white'):
    ax0 = fig.add_subplot(121)
    sns.barplot(x='expected', y=measure, data=avgdata, ci=68, order=[1.0, 0.0], 
                palette='Set2', ax=ax0, errcolor='black', edgecolor='black', linewidth=2, capsize=.2)
    if measure=='hit':
        ax0.set_ylabel('Accuracy', fontsize=30)
    elif measure=='dprime':
        ax0.set_ylabel('d\'', fontsize=30)
    elif measure=='criterion':
        ax0.set_ylabel('Criterion', fontsize=30)
    plt.yticks(fontsize=24) 
    ax0.tick_params(axis='y', direction='out', color='black', length=10, width=2)
    ax0.tick_params(axis='x', length=0)
    ax0.set_xlabel(None)
    ax0.set_xticklabels(['Cong.', 'Incong.'], fontsize=30)
    ax0.spines['left'].set_linewidth(2)
    ax0.spines['bottom'].set_linewidth(2)
    ax0.spines['right'].set_visible(False)
    ax0.spines['top'].set_visible(False)
    if measure=='hit':
        ax0.set(ylim=(0.5, 0.75))
    elif measure=='dprime':
        ax0.set(ylim=(0.0, 1.0))
    elif measure=='criterion':
        ax0.set(ylim=(0.0, 1.0))
    #with sns.axes_style('white'):
    ax1 = fig.add_subplot(122)
    sns.violinplot(y='difference', data=alldiffs, color=".8", inner=None)
    sns.stripplot(y='difference', data=alldiffs, jitter=0.07, ax=ax1, color='black', alpha=.5)
    # Get mean and 95% CI:
    meandiff = alldiffs['difference'].mean()
    tstats = pg.ttest(alldiffs['difference'], 0.0)
    ci95 = tstats['CI95%'][0]
    for tick in ax1.get_xticks():
        ax1.plot([tick-0.1, tick+0.1], [meandiff, meandiff],
                    lw=4, color='k')
        ax1.plot([tick, tick], [ci95[0], ci95[1]], lw=3, color='k')
        ax1.plot([tick-0.03, tick+0.03], [ci95[0], ci95[0]], lw=3, color='k')
        ax1.plot([tick-0.03, tick+0.03], [ci95[1], ci95[1]], lw=3, color='k')
    ax1.axhline(0.0, linestyle='--', color='black')
    plt.yticks(fontsize=24) 
    if measure=='hit':
        ax1.set_ylabel('Δ Accuracy', fontsize=30)
        if excl:
            ax1.set(ylim=(-0.2, 0.4))
        else:
            ax1.set(ylim=(-0.3, 0.4))
    elif measure=='dprime':
        ax1.set_ylabel('Δ d\'', fontsize=30)
        ax1.set(ylim=(-2., 2.))
    elif measure=='criterion':
        ax1.set_ylabel('Δ Criterion', fontsize=30)
        ax1.set(ylim=(-1.0, 1.25))
    ax1.axes_style = 'white'
    ax1.tick_params(axis='y', direction='out', color='black', length=10, width=2)
    ax1.tick_params(axis='x', length=0)
    ax1.spines['left'].set_linewidth(2)
    ax1.spines['bottom'].set_linewidth(2)
    ax1.spines['right'].set_visible(False)
    ax1.spines['bottom'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    plt.tight_layout()
    whichprob = avgdata.p_exp[0]
    if not fname:
        fname = f'{rotzoom}_p{whichprob*100:g}_{measure}.pdf'
        if not excl:
            fname.replace('.pdf', '_noexcl.pdf')
    plt.savefig(os.path.join('plots', fname))

# --------------------------------------------------------------------------------------------------------

def make_staircase_plots(allsubjdata):
    
    task = allsubjdata.task.iloc[0]
    
    fig = plt.figure(figsize=(20,30))
    #fig = plt.figure(figsize=(20,80))
    #fig = plt.figure(figsize=(20,10))
    nsubjs = allsubjdata.subject.nunique()
    n = 192
    #n = 192 * (1-p_exp)
    remove_subjs = []
    trials_missed = []
    for i, s in enumerate(list(allsubjdata.subject.unique())):
        k = allsubjdata[allsubjdata['subject']==s].hit.sum()
        #k = allsubjdata[(allsubjdata['Subject']==s)&(allsubjdata['Expected']==0)].Hit.sum()
        #print(k/n)
        thisstair = allsubjdata.loc[allsubjdata['subject'] == s]['int_diff'].values #[:20]
        #realdiff = allsubjdata.loc[allsubjdata['subject'] == s]['real_diff'].values #[:20]
        #print(np.max(thisstair))
        howmuchceil = sum(thisstair==20)
        missingtrials = pd.isna(allsubjdata[allsubjdata['subject'] == s].hit).sum()
        trials_missed.append(missingtrials)
        ax = fig.add_subplot(ceil(nsubjs/4), 4, i+1)
        if task=='rotation':
            ax.set_ylim([0, 45])
        elif task=='scale':
            ax.set_ylim([0, 0.25])
        if binom_test(k, n, p=0.5, alternative='greater')>0.05: #or missingtrials >= (len(thisstair)/20): #or howmuchceil >= len(thisstair)/20:
            ax.plot(thisstair, 'r')
            remove_subjs.append(s)
        else:
            ax.plot(thisstair, 'k')
        #if task=='rotation':
            #ax.plot(realdiff, 'b')
    plt.tight_layout()
    #plt.savefig('allstaircases.png', transparent=False)
    #plt.savefig('staircases_samediff.png', transparent=False)
    #plt.savefig('staircases_realandnotreal.png', transparent=False)
    
    return remove_subjs

# --------------------------------------------------------------------------------------------------------

def make_align_plot(avgdata, measure='hit', split=True):
    
    # Get all differences for each p(exp) and alignment
    alldiffs = []
    for (pe, al) in product(avgdata.p_exp.unique(), avgdata.aligned.unique()):
        thiscond = avgdata[(avgdata.p_exp==pe)&(avgdata.aligned==al)]
        for sub in thiscond.subject.unique():
            thisdiff = thiscond[(thiscond.subject==sub)&(thiscond.expected==1)][measure].values[0] - \
                       thiscond[(thiscond.subject==sub)&(thiscond.expected==0)][measure].values[0]
            alldiffs.append({'subject': sub, 'p_exp': pe, 'aligned': al, 'difference': thisdiff})
    alldiffs = pd.DataFrame(alldiffs)
    
    #plt.rcParams['ytick.major.size'] = 10
    #plt.rcParams['ytick.color'] = 'black'
    with sns.axes_style('white'):
        if split:
            fig = plt.figure(figsize=(18, 6))
            for i, pe in enumerate([0.75, 0.5, 0.25]):
                plt.rcParams['ytick.left'] = True
                plt.rcParams['ytick.direction'] = 'in'
                #plt.rcParams['ytick.minor.size'] = 3
                #plt.rcParams['ytick.major.size'] = 6
                plt.rcParams['axes.linewidth'] = 1.5
                ax = fig.add_subplot(1, 3, i+1)
                sns.violinplot(x='aligned', y='difference', order=[True, False], 
                               data=alldiffs[alldiffs['p_exp']==pe], inner=None, palette='Paired')
                sns.stripplot(x='aligned', y='difference', order=[True, False], 
                              data=alldiffs[alldiffs['p_exp']==pe], 
                              jitter=0.07, ax=ax, color='black', alpha=.5)
                
                # Get mean and 95% CI:
                meandiffs = [alldiffs[(alldiffs['p_exp']==pe)&(alldiffs['aligned']==al)]['difference'].mean() for al in [True, False]]
                ci95 = [pg.ttest(alldiffs[(alldiffs['p_exp']==pe)&(alldiffs['aligned']==al)]['difference'], 0.0)['CI95%'][0] for al in [True, False]]
                #ax.xaxis.set_major_locator(FixedLocator([1.5, 2.0]))
                ax.margins(x=0.2)
                for tick in ax.get_xticks():
                    ax.plot([tick-0.1, tick+0.1], [meandiffs[tick], meandiffs[tick]],
                            lw=4, color='k')
                    ax.plot([tick, tick], [ci95[tick][0], ci95[tick][1]], lw=3, color='k')
                    ax.plot([tick-0.01, tick+0.01], [ci95[tick][0], ci95[tick][0]], lw=3, color='k')
                    ax.plot([tick-0.01, tick+0.01], [ci95[tick][1], ci95[tick][1]], lw=3, color='k')
                if measure=='hit':
                    ylab = 'Δ Accuracy'
                    ax.set(ylim=(-0.7, 0.7))
                elif measure=='dprime':
                    ylab = 'Δ d\''
                    ax.set(ylim=(-3, 3))
                elif measure=='criterion':
                    ylab = 'Δ Criterion'
                    ax.set(ylim=(-1.5, 1.5))
                if i==0:
                    ax.set_ylabel(ylab, fontsize=24)
                else:
                    ax.set_ylabel('')
                plt.yticks(fontsize=18)
                ax.set_xlabel(None)
                ax.set_xticklabels(['Aligned', 'Misaligned'], fontsize=24)
                ax.axhline(0.0, linestyle='--', color='black', linewidth=1.5)
                ax.yaxis.set_tick_params(width=1.5, length=5)
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
        else:
            fig = plt.figure(figsize=(10, 6))
            plt.rcParams['ytick.left'] = True
            plt.rcParams['ytick.direction'] = 'in'
            #plt.rcParams['ytick.minor.size'] = 3
            #plt.rcParams['ytick.major.size'] = 6
            plt.rcParams['axes.linewidth'] = 1.5
            ax = fig.add_subplot(1, 1, 1)
            sns.violinplot(x='p_exp', y='difference', hue='aligned',  
                            order=[0.75, 0.5, 0.25], hue_order=[True, False], 
                            width= 0.8,data=alldiffs, ax=ax,
                            inner=None, palette='Paired')
            sns.stripplot(x='p_exp', y='difference', hue='aligned', 
                            order=[0.75, 0.5, 0.25], hue_order=[True, False],  
                            data=alldiffs,  ax=ax, dodge=True,
                            jitter=0.07, color='black', alpha=.3)
            ax.legend_.remove()
            meandiffs = []
            ci95 = []
            for pe in [0.75, 0.5, 0.25]:
                # Get mean and 95% CI:
                meandiffs.append([alldiffs[(alldiffs['p_exp']==pe)&(alldiffs['aligned']==al)]['difference'].mean() for al in [True, False]])
                ci95.append([pg.ttest(alldiffs[(alldiffs['p_exp']==pe)&(alldiffs['aligned']==al)]['difference'], 0.0)['CI95%'][0] for al in [True, False]])
            #ax.xaxis.set_major_locator(FixedLocator([1.5, 2.0]))
            ax.margins(x=0.2)
            for tick in ax.get_xticks():
                # Aligned:
                ax.plot([tick-0.25, tick-0.15], [meandiffs[tick][0], meandiffs[tick][0]], lw=3, color='k')
                ax.plot([tick-0.2, tick-0.2], [ci95[tick][0][0], ci95[tick][0][1]], lw=2, color='k')
                ax.plot([tick-0.21, tick-0.19], [ci95[tick][0][0], ci95[tick][0][0]], lw=2, color='k')
                ax.plot([tick-0.21, tick-0.19], [ci95[tick][0][1], ci95[tick][0][1]], lw=2, color='k')

                # Misaligned:
                ax.plot([tick+0.15, tick+0.25], [meandiffs[tick][1], meandiffs[tick][1]], lw=3, color='k')
                ax.plot([tick+0.2, tick+0.2], [ci95[tick][1][0], ci95[tick][1][1]], lw=2, color='k')
                ax.plot([tick+0.19, tick+0.21], [ci95[tick][1][0], ci95[tick][1][0]], lw=3, color='k')
                ax.plot([tick+0.19, tick+0.21], [ci95[tick][1][1], ci95[tick][1][1]], lw=3, color='k')
            if measure=='hit':
                ylab = 'Δ Accuracy'
                ax.set(ylim=(-0.7, 0.7))
            elif measure=='dprime':
                ylab = 'Δ d\''
                ax.set(ylim=(-3, 3))
            elif measure=='criterion':
                ylab = 'Δ Criterion'
                ax.set(ylim=(-1.5, 1.5))
            ax.set_ylabel(ylab, fontsize=20)
            plt.yticks(fontsize=14)
            ax.set_xlabel(None)
            ax.set_xticklabels(['Exp. 1', 'Exp. 2', 'Exp. 3'], fontsize=20)
            ax.axhline(0.0, linestyle='--', color='black', linewidth=1.5)
            ax.yaxis.set_tick_params(width=1.5, length=5)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

    plt.tight_layout()
    plt.margins(x=0.08)
    figname = f'plots/aligned_misaligned_{measure:s}.pdf'
    if not split:
        figname.replace('.pdf', '_single.pdf')
    plt.savefig(figname)
    return alldiffs

# --------------------------------------------------------------------------------------------------------

def make_align_plot_together(avgdata, measure='hit', split=True):
    '''
    Collapse across experiments, show results for aligned/misaligned,
    congruent/incongruent (not just cong-incong differences)
    '''
    
    # Get all differences for each p(exp) and alignment
    alldiffs = []
    for (pe, al) in product(avgdata.p_exp.unique(), avgdata.aligned.unique()):
        thiscond = avgdata[(avgdata.p_exp==pe)&(avgdata.aligned==al)]
        for sub in thiscond.subject.unique():
            thisdiff = thiscond[(thiscond.subject==sub)&(thiscond.expected==1)][measure].values[0] - \
                       thiscond[(thiscond.subject==sub)&(thiscond.expected==0)][measure].values[0]
            alldiffs.append({'subject': sub, 'p_exp': pe, 'aligned': al, 'difference': thisdiff})
    alldiffs = pd.DataFrame(alldiffs)
    
    # p75means.groupby(['subject']).mean().reset_index()
    avgdata = avgdata.groupby(['subject', 'expected', 'aligned']).mean().reset_index()
    pal = [[list(sns.color_palette('Paired'))[0], list(sns.color_palette('Paired'))[6]],
           [list(sns.color_palette('Paired'))[1], list(sns.color_palette('Paired'))[7]]]
    
    #plt.rcParams['ytick.major.size'] = 10
    #plt.rcParams['ytick.color'] = 'black'
    with sns.axes_style('white'):
        fig = plt.figure(figsize=(7, 6))
        plt.rcParams['ytick.left'] = True
        plt.rcParams['ytick.direction'] = 'out'
        #plt.rcParams['ytick.minor.size'] = 3
        #plt.rcParams['ytick.major.size'] = 6
        plt.rcParams['axes.linewidth'] = 1.5
        ax = fig.add_subplot(1, 1, 1)
        sns.barplot(x='aligned', y=measure, hue='expected', data=avgdata, 
                    ci=68, order=[True, False], hue_order=[1.0, 0.0],
                    palette='gray', #palette='Paired', 
                    ax=ax, errcolor='black', 
                    edgecolor='black', linewidth=2, capsize=.2)
        for bar_group, p in zip(ax.containers, pal):
            for bar, col in zip(bar_group, p):
                bar.set_facecolor(col)
        # sns.violinplot(x='aligned', y=measure, hue='expected',  
        #                 order=[True, False], hue_order=[1, 0], 
        #                 width= 0.8, data=avgdata, ax=ax,
        #                 inner=None, palette='Paired')
        # sns.stripplot(x='aligned', y=measure, hue='expected', 
        #                 order=[True, False], hue_order=[1, 0],  
        #                 data=avgdata,  ax=ax, dodge=True,
        #                 jitter=0.07, color='black', alpha=.3)
        ax.legend_.remove()
        # meandiffs = []
        # ci95 = []
        # for al in [True, False]:
        #     # Get mean and 95% CI:
        #     meandiffs.append([avgdata[(avgdata['aligned']==al)&(avgdata['expected']==e)][measure].mean() for e in [1, 0]])
        #     ci95.append([pg.ttest(avgdata[(avgdata['aligned']==al)&(avgdata['expected']==e)][measure], 0.0)['CI95%'][0] for e in [1, 0]])
        #ax.xaxis.set_major_locator(FixedLocator([1.5, 2.0]))
        # ax.margins(x=0.2)
        # for tick in ax.get_xticks():
        #     # Aligned:
        #     ax.plot([tick-0.25, tick-0.15], [meandiffs[tick][0], meandiffs[tick][0]], lw=3, color='k')
        #     ax.plot([tick-0.2, tick-0.2], [ci95[tick][0][0], ci95[tick][0][1]], lw=2, color='k')
        #     ax.plot([tick-0.21, tick-0.19], [ci95[tick][0][0], ci95[tick][0][0]], lw=2, color='k')
        #     ax.plot([tick-0.21, tick-0.19], [ci95[tick][0][1], ci95[tick][0][1]], lw=2, color='k')

        #     # Misaligned:
        #     ax.plot([tick+0.15, tick+0.25], [meandiffs[tick][1], meandiffs[tick][1]], lw=3, color='k')
        #     ax.plot([tick+0.2, tick+0.2], [ci95[tick][1][0], ci95[tick][1][1]], lw=2, color='k')
        #     ax.plot([tick+0.19, tick+0.21], [ci95[tick][1][0], ci95[tick][1][0]], lw=3, color='k')
        #     ax.plot([tick+0.19, tick+0.21], [ci95[tick][1][1], ci95[tick][1][1]], lw=3, color='k')
        if measure=='hit':
            ylab = 'Accuracy'
            ax.set(ylim=(0.5, 0.8))
        elif measure=='dprime':
            ylab = 'd\''
            ax.set(ylim=(0.0, 1.0))
        elif measure=='criterion':
            ylab = 'Criterion'
            ax.set(ylim=(0.0, 1.0))
        ax.set_ylabel(ylab, fontsize=20)
        plt.yticks(fontsize=16)
        ax.set_xlabel(None)
        ax.set_xticklabels(['Aligned', 'Misaligned'], fontsize=20)
        #ax.axhline(0.0, linestyle='--', color='black', linewidth=1.5)
        ax.yaxis.set_tick_params(width=1.5, length=5)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        #ax.spines['bottom'].set_visible(False)

    plt.tight_layout()
    plt.margins(x=0.08)
    figname = f'plots/aligned_misaligned_together_{measure:s}.pdf'
    plt.savefig(figname)
    #return alldiffs

# --------------------------------------------------------------------------------------------------------
    
def running_mean(x, N):
    cumsum = np.nancumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

# --------------------------------------------------------------------------------------------------------

def get_measures_in_time(alldata, winsize=24):
    
    allhits = []
    alldprimes = []
    allcrits = []
    allps = []
    allexps = []
    allsubs = []
    alltrialnos = []
    
    for p in alldata.p_exp.unique():
        for exp in [0, 1]:
            thiscond = alldata[(alldata['p_exp']==p)&(alldata['expected']==exp)]
            for i, s in enumerate(thiscond.subject.unique()):
                thissub = thiscond[thiscond['subject']==s]
                thesehits = running_mean(list(thissub['hit'].values), winsize)
                thesedprm = running_mean(list(thissub['dprime'].values), winsize)
                thesecrits = running_mean(list(thissub['criterion'].values), winsize)
                assert(len(thesehits)==len(thesedprm)==len(thesecrits))
                ntrials = len(thesehits)
                
                allhits.extend(thesehits)
                alldprimes.extend(thesedprm)
                allcrits.extend(thesecrits)
                allps.extend([p]*ntrials)
                allexps.extend([exp]*ntrials)
                allsubs.extend([i+1]*ntrials)
                alltrialnos.extend(range(ntrials))
    
    tseriesdf = {'p_exp': allps, 'expected': allexps, 'subject': allsubs,
                 'trialno': alltrialnos, 'hit': allhits, 'dprime': alldprimes,
                 'criterion': allcrits}
    tseriesdf = pd.DataFrame(tseriesdf)
    return tseriesdf

# --------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    
    datadir = '/Users/giacomoaldegheri/scenerotation_2021/data/'
    allfiles = glob(os.path.join(datadir, '*.csv'))
    allfiles = sorted(allfiles, key = lambda file: os.path.getctime(file))
    allfiles = [f for f in allfiles if (('presurvey' not in f) & ('posttraining' not in f))]
    
    allsubjdata = pd.DataFrame()
    allsanchecks = pd.DataFrame()
    allsurveys = pd.DataFrame()
    
    for i, f in enumerate(tqdm(allfiles)):
        this_rawdata = pd.read_csv(f, engine='python', error_bad_lines=False)
        this_data = cleanupdata(this_rawdata)
        if not this_data is None:
            assert(len(this_data)==192)
            this_data['subject'] = i+1
            this_data['date'] = this_rawdata.date.iloc[0]
            this_data['time'] = this_rawdata.starttime.iloc[0]
            #this_data['real_diff'] = this_data['real_diff'].interpolate()
            
            this_sancheck = extract_sanitychecks(this_rawdata)
            this_sancheck['subject'] = i+1
            this_sancheck['date'] = this_rawdata.date.iloc[0]
            this_sancheck['time'] = this_rawdata.starttime.iloc[0]
            
            this_survey = extract_survey(this_rawdata)
            this_survey['subject'] = i+1
            this_survey['date'] = this_rawdata.date.iloc[0]
            this_survey['time'] = this_rawdata.starttime.iloc[0]
            allsubjdata = pd.concat([allsubjdata, this_data], ignore_index=True)
            allsanchecks = pd.concat([allsanchecks, this_sancheck], ignore_index=True)
            allsurveys = pd.concat([allsurveys, this_survey], ignore_index=True)
            
    allsubjdata.to_csv('data/allsubjdata.csv', index=False)
    allsanchecks.to_csv('data/allsanchecks.csv', index=False)
    allsurveys.to_csv('data/allsurveys.csv', index=False)