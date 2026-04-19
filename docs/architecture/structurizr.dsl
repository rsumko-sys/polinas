workspace {
  model {
    user = person "User" "End user of the application"
    polinas = softwareSystem "POLINAS DIARIES" "Horse training app (FastAPI + static UI)"
    web = container polinas "Web Application" "FastAPI" "Serves REST API and static UI"
    db = container polinas "Database" "Postgres" "Persists sessions and clubs"
    user -> web "Uses"
  }
  views {
    systemContext polinas {
      include *
      autolayout lr
    }
    theme default
  }
}
