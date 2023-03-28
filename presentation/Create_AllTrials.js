
var Create_AllTrials = (function()
{

  var my = {};

  my.run = function(Opt)
  {

    if (!('Demo' in Opt)) {Opt.Demo = false};

    var Scenes;
    if (Math.random() > 0.5)
    { Scenes = [1, 3, 7, 20]; }
    else
    { Scenes = [2, 4, 10, 18]; }

    const InitViews = [0, 60, 120, 180, 240, 300];

    const FinalViews = [30, 90];

    if (Opt.Demo==true)
    { var NTrials = Opt.NDemoTrials; }
    else
    { var NTrials = InitViews.length * FinalViews.length * (24/InitViews.length); }

    // pick scenes
    var AllScenes = [];
    for (var i = 0; i < NTrials; i++)
    {
      var TheseScenes = GA_utils.shuffle([0, 1, 2, 3]);
      if (i != 0)
      {
        while (TheseScenes[0]==AllScenes.slice(-1)[0])
        {
          TheseScenes = GA_utils.shuffle([0, 1, 2, 3]);
        }
      }
      AllScenes = AllScenes.concat(TheseScenes);
    }
    //console.log(AllScenes);

    if (Opt.Demo==true)
    {
      var AllTrials = Array(NTrials);

      // Linearly decrease probe durations
      // from 300 to 50 (final duration in the experiment):
      const trainDurations = GA_utils.split(50, 300, NTrials).reverse();

      // in the demo, unlike in the main experiment, views are not
      // balanced within expected and unexpected
      var AllExps = Array(NTrials).fill(0);
      for (var i = 0; i < (Opt.P_Exp * NTrials); i++)
      { AllExps[i] = 1; }

      var SameDiff = Array(NTrials).fill(0);
      for (var i = 0; i < NTrials; i++)
      { if (i % 2 == 0) { SameDiff[i] = 1; } }

      GA_utils.double_shuffle(AllExps, SameDiff);

      for (var i = 0; i < NTrials; i++)
      {
        AllTrials[i] = {
          Scene: Scenes[AllScenes[i]],
          InitView: jsPsych.randomization.sampleWithoutReplacement(InitViews, 1)[0],
          FinalView: jsPsych.randomization.sampleWithoutReplacement(FinalViews, 1)[0],
          Expected: AllExps[i],
          SameDiff: SameDiff[i],
          ProbeDuration: trainDurations[i]
        };
      }
    }
    else
    {
      var AllViews = GA_utils.reparray([...GA_utils.cartesian(InitViews, FinalViews)], (24/InitViews.length));

      for (i = 0; i < AllViews.length; i++)
      {
        if (i < AllViews.length * Opt.P_Exp)
        {AllViews[i] = AllViews[i].concat(1);}
        else {AllViews[i] = AllViews[i].concat(0);}
      }

      var ViewsPerScene = [];
      for (i = 0; i < (24/InitViews.length); i++)
      {
        ViewsPerScene.push(GA_utils.shuffle(AllViews.slice()));
      }

      var SceneIndexes = Array(4).fill(0);

      var AllTrials = Array(AllScenes.length);

      for (var i = 0; i < AllScenes.length; i++)
      {
        AllTrials[i] = {
          Scene: Scenes[AllScenes[i]],
          InitView: ViewsPerScene[AllScenes[i]][SceneIndexes[AllScenes[i]]][0],
          FinalView: ViewsPerScene[AllScenes[i]][SceneIndexes[AllScenes[i]]][1],
          Expected: ViewsPerScene[AllScenes[i]][SceneIndexes[AllScenes[i]]][2],
          ProbeDuration: 50
        };
        SceneIndexes[AllScenes[i]] += 1;
      }
    }

    for (var i = 0; i < AllTrials.length; i++)
    {
      // Get view sequence:
      if (AllTrials[i].FinalView==30)
        { possibleviews = [15, 20, 25]; }
      else if (AllTrials[i].FinalView==90)
        { possibleviews = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60]; }
      var thisseq = [0];

      thisseq = thisseq.concat(jsPsych.randomization.sampleWithoutReplacement(possibleviews, 3).sort());
      thisseq.push(AllTrials[i].FinalView);

      // pre-specify image files:
      for (var im = 0; im < 5; im++)
      {
        AllTrials[i][`img_${im+1}`] = [Opt.StimDir,
        `/Scene${AllTrials[i].Scene}_${AllTrials[i].InitView}_`,
        `${thisseq[im].toString().padStart(4, '0')}.png`].join(``);
      }
    }

    return AllTrials;

  }

  return my;

})();
