# import pyttsx3

# def speak(text):
#     engine = pyttsx3.init(driverName="espeak")
#     engine.say(text)
#     engine.runAndWait()


print("welcome to talking calculator!")



while True:

    num1 = float(input("enter the first number:"))
    num2 = float(input("enter the second number:"))
    opr = input("enter the operation:")
    result =0

    if opr == "exit":
       print("thankss")
      #  speak("thank you")
       break
    if opr =="+":
      result = num1 + num2
    elif opr == "-":
      result = num1 - num2
    elif opr == "*":
      result = num1 * num2
    elif opr == "/":
      result = num1 / num2
    elif opr == "%":
      result = num1 % num2
    else:
       print("invalid operator")
       continue
    print("the result is", result)
    # speak(f"the result is{result}")
    