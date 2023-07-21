all: build

build: form1_ui_to_py form2_ui_to_py create_exe

test: form1_ui_to_py form2_ui_to_py 

form1_ui_to_py:
	pyuic5 forms/start.ui -o forms/start.py

form2_ui_to_py:
	pyuic5 forms/game.ui -o forms/game.py

create_exe:
	pyinstaller src/main.py --noconsole --add-data "pictures;pictures" --add-data "forms;forms" --add-data "icons;icons" --icon=icons/icon.ico --name Yamb --noconfirm

clean:
	rmdir /s /q build dist