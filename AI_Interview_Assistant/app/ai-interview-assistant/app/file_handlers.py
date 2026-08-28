def load_json_file(file_path):
    if not file_path.exists():
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        st.error(f"Unable to load {file_path.name}: {e}")
        return None


def load_evaluation_report():
    return load_json_file(Path.cwd() / "data" / "evaluation_report.json")


def load_feedback_report():
    return load_json_file(Path.cwd() / "data" / "feedback_report.json")