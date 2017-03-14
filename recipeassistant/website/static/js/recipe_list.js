// Recipe List Script

$(document).ready(function(){
    var json_data;
    $.ajax({
        dataType: "json",
        url: 'https://0s2cp85xw1.execute-api.us-east-1.amazonaws.com/prod/RecipeUpdate?TableName=Recipes',
        data: "",
        success: function(data) {
            json_data = data;
        }
    });
    var recipeItem;
    var i = 0;
    for (recipeItem in json_data.Items) {
        //modal i recipeTitle = recipeItem.RecipeName;
        //modal i directions = recipeItem.Directions;
        //modal i imgURL = recipeItem.imgURL
        //modal i ingredients = recipeItem.Ingredients;
    }
});
