CC := gcc

run: build
	./{project_name}

build:
	@$(CC) -o {project_name} src/main.c

clean:
	@-rm {project_name}

.PHONY: build clean run
