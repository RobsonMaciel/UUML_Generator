// File.h
#pragma once

#include "CoreMinimal.h"
#include "File.generated.h"

UCLASS()
class YOURPROJECT_API AFile {
    GENERATED_BODY()

public:
    AFile();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "File")
    FString Path;

    UFUNCTION(BlueprintCallable, Category = "File")
    void Read();

    UFUNCTION(BlueprintCallable, Category = "File")
    void Write();

    UFUNCTION(BlueprintCallable, Category = "File")
    void Delete();
}
