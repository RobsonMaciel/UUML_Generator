// Directory.h
#pragma once

#include "CoreMinimal.h"
#include "Directory.generated.h"

UCLASS()
class YOURPROJECT_API ADirectory {
    GENERATED_BODY()

public:
    ADirectory();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Directory")
    FString Path;

    UFUNCTION(BlueprintCallable, Category = "Directory")
    void Create();

    UFUNCTION(BlueprintCallable, Category = "Directory")
    void Delete();
}
