import random

choices = ["Stone", "Paper", "Scissors"]
user_score = 0
computer_score = 0
rounds = 3

print("Welcome to Best of 3 Stone-Paper-Scissors Game!\n")

for round_no in range(1, rounds + 1):
    print(f"Round {round_no}")
    computer = random.choice(choices)
    user_input = input("Enter your choice (Stone/Paper/Scissors): ").capitalize()

    if user_input not in choices:
        print("Invalid choice! Please type Stone, Paper, or Scissors.\n")
        continue

    print(f"You chose {user_input}\nComputer chose {computer}")

    if computer == user_input:
        print("It's a Draw!\n")
    elif (user_input == "Stone" and computer == "Scissors") or \
         (user_input == "Paper" and computer == "Stone") or \
         (user_input == "Scissors" and computer == "Paper"):
        print("You Win this round 🎉\n")
        user_score += 1
    else:
        print("Computer Wins this round 😢\n")
        computer_score += 1

print("Final Scores:")
print(f"You: {user_score} | Computer: {computer_score}")

if user_score > computer_score:
    print("🏆 Congratulations! You are the overall Winner!")
elif computer_score > user_score:
    print("💻 Computer Wins the Best of 3!")
else:
    print("🤝 It's a Tie overall!")
