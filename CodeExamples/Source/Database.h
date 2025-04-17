// Database.h
#pragma once

#include "CoreMinimal.h"
#include "Database.generated.h"

UCLASS()
class YOURPROJECT_API ADatabase {
    GENERATED_BODY()

public:
    ADatabase();

    UFUNCTION(BlueprintCallable, Category = "Database")
    void Connect(FString connectionString);

    UFUNCTION(BlueprintCallable, Category = "Database")
    void Query(FString sql);

    UFUNCTION(BlueprintCallable, Category = "Database")
    void Insert(FString table, FString data);
}
