// Quest.h
#pragma once

#include "CoreMinimal.h"
#include "Quest.generated.h"

UCLASS()
class YOURPROJECT_API AQuest {
    GENERATED_BODY()

public:
    AQuest();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Title;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    FString Description;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest")
    bool IsCompleted;

    UFUNCTION(BlueprintCallable, Category = "Quest")
    void StartQuest();

    UFUNCTION(BlueprintCallable, Category = "Quest")
    void CompleteQuest();

    UFUNCTION(BlueprintCallable, Category = "Quest")
    void FailQuest();

    UFUNCTION(BlueprintCallable, Category = "Quest")
    void UpdateProgress(int progress);
}
