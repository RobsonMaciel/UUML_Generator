// ResourceManager.h
#pragma once

#include "CoreMinimal.h"
#include "ResourceManager.generated.h"

UCLASS()
class YOURPROJECT_API AResourceManager {
    GENERATED_BODY()

public:
    AResourceManager();

    UFUNCTION(BlueprintCallable, Category = "Resources")
    void LoadResource(FString resourceName);

    UFUNCTION(BlueprintCallable, Category = "Resources")
    void UnloadResource(FString resourceName);

    UFUNCTION(BlueprintCallable, Category = "Resources")
    void ListResources();
}
