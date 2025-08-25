from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the Excel file once
df = pd.read_excel("KB BRICK LOCATION BY NAME EXCEL.xlsx")
sections = sorted(df['MEMORIAL PLAZA SECTION'].dropna().unique())

@app.route('/', methods=['GET', 'POST'])
def search():
    results = []
    name_query = ""
    loc_query = ""
    selected_section = ""

    if request.method == 'POST':
        name_query = request.form.get('name_query', '').strip()
        selected_section = request.form.get('section', '')

        filtered = df

        # Apply filters if provided
        if name_query:
            filtered = filtered[filtered['BRICK NAME'].str.contains(name_query, case=False, na=False)]

        if selected_section:
            filtered = filtered[filtered['MEMORIAL PLAZA SECTION'].str.strip() == selected_section.strip()]

        # Format results
        results = filtered[['BRICK NAME', 'MEMORIAL PLAZA SECTION', 'LOCATION']].to_dict(orient='records')

    return render_template('search.html', results=results, sections=sections,
                           name_query=name_query, loc_query=loc_query, selected_section=selected_section)

if __name__ == '__main__':
    app.run(debug=True)
