terraform {
  required_version = ">= 1.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {

}

resource "docker_network" "app_network" {
  name = "${var.project_name}-network"
}
