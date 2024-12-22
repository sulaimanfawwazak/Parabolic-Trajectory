import pandas as pd
import numpy as np
import random
import streamlit as st

random.seed(42)

data  = {
  'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
  'Temperature': [random.randint(20, 35) for _ in range(5)],
  'Humidity': [random.randint(40, 90) for _ in range(5)]
}

df = pd.DataFrame(data)
print(df)

print(np.random.randint(20, 30, size=5))

st.line_chart(df.set_index('Day')['Temperature'])
st.line_chart(df.set_index('Day')['Humidity'])