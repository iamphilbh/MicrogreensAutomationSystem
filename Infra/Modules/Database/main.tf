resource "azurerm_postgresql_server" "srv" {
  name                = "sqlsrv-mgas-${var.location_short}-${var.env}"
  location            = var.location
  resource_group_name = var.resource_group_name

  administrator_login          = var.sql_admin_login
  administrator_login_password = var.sql_admin_password

  sku_name   = "GP_Gen4_1"
  version    = "11"
  storage_mb = 5120

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = false

  public_network_access_enabled    = false
  ssl_enforcement_enabled          = true
  ssl_minimal_tls_version_enforced = "TLS1_2"

  tags = var.tags
}

resource "azurerm_sql_database" "db" {
  name                = "sqldb-mgas-${var.location_short}-${var.env}"
  location            = var.location 
  resource_group_name = var.resource_group_name
  server_name         = azurerm_sql_server.srv.name

  tags = var.tags

  lifecycle {
    prevent_destroy = true
  }
}