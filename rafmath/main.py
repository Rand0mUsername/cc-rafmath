from .interpreter import Interpreter

def main():
	prompt = "rafmath> "
	interpreter = Interpreter()
	while True:
		line = input(prompt)
		if line:
			output = interpreter(line)
			if output is None:
				print("Bye.")
				break
			else:
				print(output)

if __name__ == '__main__':   
        main()