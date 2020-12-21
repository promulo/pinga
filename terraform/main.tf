resource "aiven_account" "paulocompany" {
  name = "paulocompany"
}

resource "aiven_project" "pinga_dev" {
  project = "pinga-dev"
  account_id = aiven_account.paulocompany.account_id
}

resource "aiven_account_team" "pinga_admins" {
  account_id = aiven_account.paulocompany.account_id
  name = "Admins"
}

resource "aiven_account_team_project" "pinga" {
  account_id = aiven_account.paulocompany.account_id
  team_id = aiven_account_team.pinga_admins.team_id
  project_name = aiven_project.pinga_dev.project
  team_type = "admin"
}

resource "aiven_account_team_member" "paulo" {
  account_id = aiven_account.paulocompany.account_id
  team_id = aiven_account_team.pinga_admins.team_id
  # avoiding spam crawlers finding my personal e-mail on a public repo :)
  user_email = var.paulo_email
}
