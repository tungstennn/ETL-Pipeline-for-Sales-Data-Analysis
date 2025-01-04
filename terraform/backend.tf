# resource "aws_s3_bucket" "terraform_state" {
#   bucket = "tungstennn-terraform-state-bucket"
#   acl    = "private"

#   #   versioning {
#   #     enabled = true
#   #   }

#   tags = {
#     Name = "TerraformState"
#   }
# }

# # terraform {
# #   backend "s3" {
# #     bucket  = "tungstennn-terraform-state-bucket"
# #     key     = "cicd/terraform.tfstate" # Path within the bucket
# #     region  = "eu-west-2"
# #     encrypt = true # Encrypt the state file with SSE
# #   }
# # }

