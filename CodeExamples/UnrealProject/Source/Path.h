// Path.h
#pragma once

#include "CoreMinimal.h"
#include "Path.generated.h"

UCLASS()
class YOURPROJECT_API APath {
    GENERATED_BODY()

public:
    APath();

    UFUNCTION(BlueprintCallable, Category = "Path")
    FString GetFullPath(FString relativePath);

    UFUNCTION(BlueprintCallable, Category = "Path")
    FString Combine(FString path1, FString path2);
}
