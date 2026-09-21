output "message" {
  value = "Project: ${var.project_name}"
}

output "network_name" {
  value = docker_network.app_network.name
}

output "network_id" {
  value = docker_network.app_network.id
}
