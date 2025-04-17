// PlayerScore.h
#pragma once

#include "CoreMinimal.h"
#include "PlayerScore.generated.h"

UCLASS()
class YOURPROJECT_API APlayerScore {
    GENERATED_BODY()

public:
    APlayerScore();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Score")
    FString PlayerName;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Score")
    int Score;

    UFUNCTION(BlueprintCallable, Category = "Score")
    void UpdateScore(int newScore);
}
