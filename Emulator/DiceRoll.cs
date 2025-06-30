using System;
using System.Collections.Generic;

// A DiceRoll object will have a constructor with two inputs:
// an array of ints in the range 1-20 to represent the dice rolled
// an int Target to represent the SuccessValue of the roll.
// will calculate :
// NormalSuccesses DiceRoll object, if
public class DiceRoll
{
    public List<int> DiceValues;
    public int SuccessValue;
    public List<int> NormalSuccesses;
    public List<int> CriticalSuccesses;
    public int NumberOfSpecialDice;

    private DiceRoll(List<int> valuesRolledArg, int successValueArg, int numberOfSpecialDiceArg, bool needsCalculation)
    {
        this.DiceValues = new List<int>(valuesRolledArg);
        this.SuccessValue = successValueArg;
        this.NumberOfSpecialDice = numberOfSpecialDiceArg;

        if(needsCalculation)
        {
            this.Calculate();
        }
    }

    private DiceRoll(DiceRoll diceRollArg)
    {
        this.DiceValues = new List<int>(diceRollArg.DiceValues);
        this.SuccessValue = diceRollArg.SuccessValue;
        this.NormalSuccesses = new List<int>(diceRollArg.NormalSuccesses);
        this.CriticalSuccesses = new List<int>(diceRollArg.CriticalSuccesses);
        this.NumberOfSpecialDice = diceRollArg.NumberOfSpecialDice;
    }

    public DiceRoll(List<int> valuesRolledArg, int successValueArg, int numberOfSpecialDiceArg):
        this(valuesRolledArg, successValueArg, numberOfSpecialDiceArg, true)
    {
    }

    public DiceRoll(List<int> valuesRolledArg, int successValueArg):
        this(valuesRolledArg, successValueArg, 0, true)
    {
    }

    public void Calculate()
    {
        CalculateSuccessesAndCrits(this);
    }

    public static bool IsCrit(int diceValueArg, int successValueArg)
    {
        return diceValueArg == successValueArg || (successValueArg > 20 && diceValueArg <= successValueArg - 20);
    }

    public static void CalculateSuccessesAndCrits(DiceRoll diceRollArg)
    {
        List<int> successfulDice;
        List<int> critDice;
        int numberOfDiceToRemove = diceRollArg.NumberOfSpecialDice;

        if(diceRollArg.NormalSuccesses == null)
        {
            successfulDice = new List<int>();
            critDice = new List<int>();
            foreach(int diceRollValue in diceRollArg.DiceValues)
            {
                if(IsCrit(diceRollValue, diceRollArg.SuccessValue))
                {
                    critDice.Add(diceRollValue);
                }
                else if(diceRollValue <= diceRollArg.SuccessValue)
                {
                    successfulDice.Add(diceRollValue);
                }
                else
                {
                    numberOfDiceToRemove--;
                }
            }
            successfulDice.Sort();
            successfulDice.Reverse();
            while(numberOfDiceToRemove > 0)
            {
                if(successfulDice.Count > 0)
                {
                    successfulDice.RemoveAt(successfulDice.Count - 1);
                }
                else if(critDice.Count > 0)
                {
                    critDice.RemoveAt(critDice.Count - 1);
                }
                numberOfDiceToRemove--;
            }

            diceRollArg.NormalSuccesses = successfulDice;
            diceRollArg.CriticalSuccesses = critDice;
        }
    }

    public static DiceRoll operator -(DiceRoll left, DiceRoll right)
    {
        DiceRoll difference = new DiceRoll(left);
        if(right.CriticalSuccesses.Count > 0)
        {
            difference.NormalSuccesses = new List<int>{};
            difference.CriticalSuccesses = new List<int> {};
        }
        else if(right.NormalSuccesses.Count > 0)
        {
            int rightMaxValue = right.NormalSuccesses[0];
            foreach(int successValue in left.NormalSuccesses)
            {
                if(successValue < rightMaxValue)
                {
                    difference.NormalSuccesses.Remove(successValue);
                }
            }
        }
        return difference;
    }

    public static DiceRoll[] Face2Face(DiceRoll left, DiceRoll right)
    {
        DiceRoll winner = null;
        DiceRoll winnerAdjustedDiceRoll = null;
        
        DiceRoll difference = left - right;
        
        if(difference.NormalSuccesses.Count + difference.CriticalSuccesses.Count > 0)
        {
            winner = left;
            winnerAdjustedDiceRoll = difference;
        }
        else
        {
            difference = right - left;
            if(difference.NormalSuccesses.Count + difference.CriticalSuccesses.Count > 0)
            {
                winner = right;
                winnerAdjustedDiceRoll = difference;
            }
        }
        return new DiceRoll[] {winner, winnerAdjustedDiceRoll};
    }

    static void Main(string[] args)
    {
        // Replace with proper unit testing
        List<int> testerRolls = new List<int>{1,2,3,3,4};
        List<int> testerRolls2 = new List<int>{2,2,3,3,4,7,8};
        DiceRoll tester = new DiceRoll(testerRolls, 5, 1);
        DiceRoll tester2 = new DiceRoll(testerRolls, 9, 1);
        DiceRoll[] winnerAndValues = Face2Face(tester, tester2);
        string winnerStr = string.Join(",", winnerAndValues[0].DiceValues);
        string winnerAdjValuesStr = string.Join(",", winnerAndValues[1].DiceValues);
        Console.WriteLine("winnerStr: " + winnerStr);
        Console.WriteLine("winnerAdjValuesStr: " + winnerAdjValuesStr);
        // string allRollsStr = string.Join(",", tester.DiceValues);
        // string SuccessfulRollsStr = string.Join(",", tester.NormalSuccesses);
        // string CriticalSuccessesStr = string.Join(",", tester.CriticalSuccesses);
        // Console.WriteLine("All rolls: " + allRollsStr);
        // Console.WriteLine("Successful non-crit rolls: " + SuccessfulRollsStr);
        // Console.WriteLine("Crit rolls: " + CriticalSuccessesStr);
        // Console.WriteLine("1 isCrit for 22: " + IsCrit(1, 22).ToString());
        // Console.WriteLine("2 isCrit for 22: " + IsCrit(2, 22).ToString());
    }
}

// this.DiceValues = int[] DiceValues

// CalculateSuccessesAndCrits(DiceRoll rollToBeChecked, Boolean calculateSuccesses): Return DiceRoll
// There will be a method for normal rolls, which will return return a DiceRoll object that has the dice rolled at or below the target number (or have an empty array if unsuccessful). Also, number of crits will be calculated.
// input will be 1 DiceRoll object
// This could be calculated at construction, with a check if NormalSuccesses is null. This NormalSuccesses DiceRoll object is effectively all that is needed for any further calculations.
// Can handle SD here, since crit > highest number > any successful number > failed number.
// Can order the rolls, since SD will require it anyways, and will be helpful in the case of f2f. Maybe make an Ordered boolean to keep track if DiceRoll object is ordered, since sorting is unnecessary if just a Normal roll with no special dice is needed.

// There will be a method for face to face rolls, which will return a DiceRoll object that has the successful dice (or have an empty array if unsuccessful), and a True if the dice were from the first DiceRoll object, and a false if from the second DiceRoll object. Also, number of crits will be calculated. (Crit vs crit, or tie vs tie, will return a DiceRoll object with 0 crits and an empty array)
// input will be 2 DiceRoll objects

