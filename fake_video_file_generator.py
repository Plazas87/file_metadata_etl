import pathlib


def main():
    """Create directory json files as fake data."""
    for day in range(1, 31):
        if day < 10:
            day = f"0{day}"
        
        for zz in ["AM", "PM"]:
            directory = pathlib.Path(f"video_data/202301{day}{zz}")
            directory.mkdir(parents=True)
            for hour in range(0, 12):
                path = directory / f"video_{hour}.json"
                with path.open("w", encoding="utf-8") as file:
                    file.close()


if __name__ == "__main__":
    main()