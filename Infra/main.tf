provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-mgas-${var.location_short}-${var.env}"
  location = var.location
}