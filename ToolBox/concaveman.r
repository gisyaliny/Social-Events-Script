pkgTest <- function(x)
{if (!require(x))  {install.packages(x) }}

arc.progress_label('Loading required R packages...')

pkgTest('concaveman');pkgTest('dplyr')

tool_exec <- function(in_params, out_params) {
  print(paste0('Input parameter names: `', paste(names(in_params), collapse = '`, `'), '`'  ))
  print(paste0('Output parameter names: `', paste(names(out_params), collapse = '`, `'), '`'))
}

# Function to test in standalone R:
test_tool <- function(){
  # Load the arcgisbinding package...
  library(arcgisbinding)
  arc.check_product()
  temp <- getwd()



}pkgTest <- function(x)
{if (!require(x))  {install.packages(x) }}

arc.progress_label('Loading required R packages...')

pkgTest('concaveman');pkgTest('dplyr')

tool_exec <- function(in_params, out_params) {
  print(paste0('Input parameter names: `', paste(names(in_params), collapse = '`, `'), '`'  ))
  print(paste0('Output parameter names: `', paste(names(out_params), collapse = '`, `'), '`'))
}

# Function to test in standalone R:
test_tool <- function(){
  # Load the arcgisbinding package...
  library(arcgisbinding)
  arc.check_product()
  temp <- getwd()



}



# Run the test_tool() function
if (!exists("arc.env") || is.null(arc.env()$workspace)) {
  test_tool()
}




# Run the test_tool() function
if (!exists("arc.env") || is.null(arc.env()$workspace)) {
  test_tool()
}
