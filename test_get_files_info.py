from functions.get_files_info import get_files_info


def main():
    test_cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../"),
    ]

    for test_case in test_cases:
        (
            working_directory,
            directory,
        ) = test_case

        output = get_files_info(working_directory, directory)

        if directory == ".":
            print("Result for current directory:")
        else:
            print(f"Result for '{directory}' directory:")

        if output.startswith("Error"):
            print(f"    {output}")

        else:
            output_list = [f"  {line}" for line in output.splitlines()]

            for line in output_list:
                print(line)


if __name__ == "__main__":
    main()
