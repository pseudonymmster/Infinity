using System;
using System.Collections.Generic;

// A DiceRoll object will have a constructor with two inputs:
// an array of ints in the range 1-20 to represent the dice rolled
// an int Target to represent the SuccessValue of the roll.
// will calculate :
// SuccessfulDiceRolled DiceRoll object, if
public class DiceRoll
{
    public List<int> DiceValues;
    public int SuccessValue;
    public DiceRoll SuccessfulDiceRolled;
    public int NumberOfCrits;
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
        SuccessfulDiceRolled = NormalRollSuccesses(this);
    }

    public static bool IsCrit(int diceValueArg, int successValueArg)
    {
        return diceValueArg == successValueArg || (successValueArg > 20 && diceValueArg <= successValueArg - 20);
    }

    public static DiceRoll NormalRollSuccesses(DiceRoll diceRollArg)
    {
        DiceRoll DiceRollReturned;
        List<int> successfulDice;

        if(diceRollArg.SuccessfulDiceRolled == null)
        {
            successfulDice = new List<int>();
            foreach(int diceRollValue in diceRollArg.DiceValues)
            {
                if(diceRollValue <= diceRollArg.SuccessValue)
                {
                    successfulDice.Add(diceRollValue);
                    Console.WriteLine("Value is: " + diceRollValue.ToString() + " and SuccessValue: " + diceRollArg.SuccessValue.ToString() + " and isCrit" + IsCrit(diceRollValue, diceRollArg.SuccessValue));
                    if(IsCrit(diceRollValue, diceRollArg.SuccessValue))
                    {
                        diceRollArg.NumberOfCrits++;
                    }
                }
            }
            successfulDice.Sort();
            DiceRollReturned = new DiceRoll(successfulDice, diceRollArg.SuccessValue, diceRollArg.NumberOfSpecialDice, false);
            DiceRollReturned.SuccessfulDiceRolled = DiceRollReturned;
            DiceRollReturned.NumberOfCrits = diceRollArg.NumberOfCrits;
        }
        else
        {
            DiceRollReturned = diceRollArg.SuccessfulDiceRolled;
        }
        return DiceRollReturned.SuccessfulDiceRolled;
    }

    static void Main(string[] args)
    {
        // Replace with proper unit testing
        List<int> testerRolls = new List<int>{1,2,3,4};
        DiceRoll tester = new DiceRoll(testerRolls, 22);
        string allRollsStr = string.Join(",", tester.DiceValues);
        string SuccessfulRollsStr = string.Join(",", tester.SuccessfulDiceRolled.DiceValues);
        string numOfCritsStr = tester.NumberOfCrits.ToString();
        Console.WriteLine("All rolls: " + allRollsStr);
        Console.WriteLine("Successful rolls: " + SuccessfulRollsStr);
        Console.WriteLine("Number of Crits: " + numOfCritsStr);
        Console.WriteLine("1 isCrit for 22: " + IsCrit(1, 22).ToString());
        Console.WriteLine("2 isCrit for 22: " + IsCrit(2, 22).ToString());
    }
}

// this.DiceValues = int[] DiceValues

// NormalRollSuccesses(DiceRoll rollToBeChecked, Boolean calculateSuccesses): Return DiceRoll
// There will be a method for normal rolls, which will return return a DiceRoll object that has the dice rolled at or below the target number (or have an empty array if unsuccessful). Also, number of crits will be calculated.
// input will be 1 DiceRoll object
// This could be calculated at construction, with a check if SuccessfulDiceRolled is null. This SuccessfulDiceRolled DiceRoll object is effectively all that is needed for any further calculations.
// Can handle SD here, since crit > highest number > any successful number > failed number.
// Can order the rolls, since SD will require it anyways, and will be helpful in the case of f2f. Maybe make an Ordered boolean to keep track if DiceRoll object is ordered, since sorting is unnecessary if just a Normal roll with no special dice is needed.

// There will be a method for face to face rolls, which will return a DiceRoll object that has the successful dice (or have an empty array if unsuccessful), and a True if the dice were from the first DiceRoll object, and a false if from the second DiceRoll object. Also, number of crits will be calculated. (Crit vs crit, or tie vs tie, will return a DiceRoll object with 0 crits and an empty array)
// input will be 2 DiceRoll objects

