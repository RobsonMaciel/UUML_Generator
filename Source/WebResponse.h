// WebResponse.h
#pragma once

#include "CoreMinimal.h"
#include "WebResponse.generated.h"

UCLASS()
class YOURPROJECT_API AWebResponse {
    GENERATED_BODY()

public:
    AWebResponse();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Network")
    FString Data;

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Parse();
}
