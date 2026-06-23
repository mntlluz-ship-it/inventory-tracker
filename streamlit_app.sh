#!/usr/bin/env bash

# Script para lanzar la app Streamlit con puerto configurable.
# Uso: PORT=8502 ./streamlit_app.sh

PORT=${PORT:-8501}
exec streamlit run streamlit_app.py --server.port "$PORT"
#!/usr/bin/env bash

# Script para lanzar la app Streamlit con puerto configurable.
# Uso: PORT=8502 ./streamlit_app.sh

PORT=${PORT:-8501}
exec streamlit run streamlit_app.py --server.port "$PORT"
