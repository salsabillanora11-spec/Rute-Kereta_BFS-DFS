import sys
from rich import print  # type: ignore

from time import sleep 

def hide_cursor():
      """Sembunyikan cursor di terminal"""
      sys.stdout.write("\033[?25l")
      sys.stdout.flush()

def show_cursor():
      """Tampilkan cursor lagi"""
      sys.stdout.write("\033[?25h")
      sys.stdout.flush()

def printLyrics():
      lines = [
            ("I Wanna da-", 0.06),
            ("I Wanna dance in the lights", 0.05),
            ("I Wanna ro-", 0.07),
            ("I Wanna rock your body", 0.08),
            ("I Wanna go", 0.08),
            ("I Wanna go for a ride", 0.68),
            ("Hope in the music and", 0.07),
            ("Rock your body", 0.08),
            ("Rock that body", 0.069),
            ("come on, come on", 0.035),
      ]

      delays = [0.2, 1, 0.2, 1, 0.2, 0.8, 0.2, 0.5, 0.18, 0.1]

      hide_cursor()

      try:
            for i, (line, char_delay) in enumerate(lines):
                  for char in line:
                        if line == "Rock your body":
                              print(f"[orange4]{char}[/orange4]", end='')
                        else: 
                              print(f"[bold][gold3]{char}[/bold][/gold3]", end='')
                        sys.stdout.flush()
                        sleep(char_delay)
                  print()
                  sleep(delays[i])
      finally:
            show_cursor()
            
printLyrics()