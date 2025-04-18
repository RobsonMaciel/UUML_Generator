// URL.h
#pragma once

#include "CoreMinimal.h"
#include "URL.generated.h"

UCLASS()
class YOURPROJECT_API UURL : public UObject {
    GENERATED_BODY()

public:
    UURL();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Network")
    FString Address;

    UFUNCTION(BlueprintCallable, Category = "Network")
    void Open();
}
