
const arrSum = arr => arr.reduce((a,b) => a + b, 0);

var prevInt = 0;
var currentInt = stair_params.startingInt_train;
var nextInt = 0; //stair_params.startingInt;
var staircaseChecker = []; // for assessing whether the value should move up/down/stay
var staircaseIndex = 0; // index for the current staircase
var n_Reversals = 0;
// reversal: ((prevInt < currentInt) && (nextInt < currentInt)) || ((prevInt > currentInt) && (nextInt > currentInt))

function resetStair()
{
  currentInt = stair_params.startingInt_main; // maybe different ones for training and main exp?
  staircaseChecker = [];
  staircaseIndex = 0;
  n_Reversals = 0;
};

function updateInt()
{
  staircaseChecker[staircaseIndex] = 1 - gaveCorrect;
  staircaseIndex += 1;
  if (n_Reversals < 3)
  { var this_stepsize = stair_params.stepSize; }
  else { var this_stepsize = stair_params.stepSize/2; }
  // increase if they got last trial incorrect
  if (arrSum(staircaseChecker) == 1)
  {
    nextInt = currentInt + this_stepsize; // increase int
    if (nextInt > stair_params.maxInt)
    {
      nextInt = stair_params.maxInt; // upper bound
    }
    staircaseChecker = []; // reset staircase checker
    staircaseIndex = 0; // reset staircase index
  }
  // decrease if they got the last N trials correct, else do nothing
  else if (arrSum(staircaseChecker)==0)
  {
    if (staircaseChecker.length==stair_params.ndown)
    {
      nextInt = currentInt - this_stepsize; // decrease int if last trial was correct
      if (nextInt < stair_params.minInt)
      {
        nextInt = stair_params.minInt; // lower bound
      }
      staircaseChecker = []; // reset staircase checker
      staircaseIndex = 0; // reset staircase index
    } else {
      // do nothing
      nextInt = currentInt;
    }
  }
  else {
      return false; // shouldn't ever be different than 1 or 0
  }
  if (prevInt != 0) // = if not first trial
  {
      if (((prevInt < currentInt) && (nextInt < currentInt)) || ((prevInt > currentInt) && (nextInt > currentInt)))
      {
        n_Reversals += 1;
      }
  }
  // update:
  if (!(training_session))
  {
    console.log("current int: ", currentInt);
    console.log("next int: ", nextInt);
    prevInt = currentInt;
    currentInt = nextInt;
  } else {
    nextInt = currentInt;
    console.log("current int: ", currentInt);
    console.log("next int: ", nextInt);
    prevInt = currentInt;
  }
};

/*
var staircase_assess = {
  type: 'call-function',
  func: updateInt
};
*/
