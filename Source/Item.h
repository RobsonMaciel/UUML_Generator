// Item.h
#pragma once

#include "CoreMinimal.h"
#include "Item.generated.h"

UCLASS()
class YOURPROJECT_API AItem {
    GENERATED_BODY()

public:
    AItem();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Item")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Item")
    FString Description;

    UFUNCTION(BlueprintCallable, Category = "Item")
    void Use();

    UFUNCTION(BlueprintCallable, Category = "Item")
    void Discard();
}
